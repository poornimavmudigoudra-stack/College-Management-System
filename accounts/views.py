from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q, Sum
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from attendance.models import Attendance
from courses.models import Course, Department, Subject
from examinations.models import Exam, Mark
from faculty.models import Faculty
from fees.models import Fee, Payment
from notices.models import Notice
from students.models import Student

from .forms import LoginForm, RegisterForm, StyledPasswordChangeForm, UserUpdateForm


def home(request):
    context = {
        "notices": Notice.objects.for_user(request.user)[:4],
        "student_count": Student.objects.count(),
        "faculty_count": Faculty.objects.count(),
        "course_count": Course.objects.count(),
        "department_count": Department.objects.count(),
    }
    return render(request, "home.html", context)


class CollegeLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().display_name}!")
        return super().form_valid(form)


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registration successful. An administrator will link your student record shortly.")
        return redirect("accounts:dashboard")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    form = UserUpdateForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")
    context = {
        "form": form,
        "student": getattr(request.user, "student_profile", None),
        "faculty": getattr(request.user, "faculty_profile", None),
    }
    return render(request, "accounts/profile.html", context)


@login_required
def change_password(request):
    form = StyledPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # keep the user logged in
        messages.success(request, "Your password was changed successfully.")
        return redirect("accounts:profile")
    return render(request, "accounts/change_password.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    if user.is_admin_user:
        return _admin_dashboard(request)
    if user.is_faculty:
        return _faculty_dashboard(request)
    return _student_dashboard(request)


def _admin_dashboard(request):
    today = timezone.localdate()
    total_fees = Fee.objects.aggregate(total=Sum("amount"))["total"] or 0
    collected = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    todays_attendance = Attendance.objects.filter(date=today)
    present_today = todays_attendance.filter(status__in=Attendance.PRESENT_STATUSES).count()

    course_stats = Course.objects.annotate(num_students=Count("students")).order_by("name")
    context = {
        "student_count": Student.objects.count(),
        "faculty_count": Faculty.objects.count(),
        "course_count": Course.objects.count(),
        "subject_count": Subject.objects.count(),
        "total_fees": total_fees,
        "collected": collected,
        "pending": total_fees - collected,
        "attendance_today": todays_attendance.count(),
        "present_today": present_today,
        "recent_students": Student.objects.select_related("user", "course").order_by("-id")[:5],
        "recent_payments": Payment.objects.select_related("fee__student__user").order_by("-payment_date", "-id")[:5],
        "upcoming_exams": Exam.objects.filter(date__gte=today).select_related("subject").order_by("date")[:5],
        "notices": Notice.objects.for_user(request.user)[:5],
        "chart_data": {
            "labels": [c.code for c in course_stats],
            "values": [c.num_students for c in course_stats],
        },
    }
    return render(request, "dashboard/admin_dashboard.html", context)


def _faculty_dashboard(request):
    today = timezone.localdate()
    faculty = getattr(request.user, "faculty_profile", None)
    subjects = Subject.objects.filter(faculty=faculty).select_related("course") if faculty else Subject.objects.none()
    subjects = subjects.annotate(
        marked_today=Count("attendance_records", filter=Q(attendance_records__date=today)),
    )
    context = {
        "faculty": faculty,
        "subjects": subjects,
        "upcoming_exams": Exam.objects.filter(subject__in=subjects, date__gte=today).select_related("subject").order_by("date")[:5],
        "pending_marks": Exam.objects.filter(subject__in=subjects, date__lte=today, marks__isnull=True).distinct().count(),
        "notices": Notice.objects.for_user(request.user)[:5],
        "today": today,
    }
    return render(request, "dashboard/faculty_dashboard.html", context)


def _student_dashboard(request):
    today = timezone.localdate()
    student = getattr(request.user, "student_profile", None)
    context = {"student": student, "notices": Notice.objects.for_user(request.user)[:5]}
    if student:
        fees = Fee.objects.filter(student=student).with_paid_total()
        subjects = Subject.objects.filter(course=student.course, semester=student.semester)
        context.update({
            "attendance": student.attendance_summary(),
            "threshold": settings.ATTENDANCE_THRESHOLD,
            "subjects": subjects.select_related("faculty__user"),
            "recent_marks": Mark.objects.filter(student=student).select_related("exam__subject").order_by("-exam__date")[:5],
            "upcoming_exams": Exam.objects.filter(subject__in=subjects, date__gte=today).select_related("subject").order_by("date")[:5],
            "fee_due": sum(fee.balance for fee in fees),
        })
    return render(request, "dashboard/student_dashboard.html", context)


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
