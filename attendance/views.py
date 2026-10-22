from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from accounts.decorators import staff_required
from courses.models import Subject
from students.models import Student

from .forms import AttendanceFilterForm
from .models import Attendance


def subjects_for(user):
    """Subjects a user may work with: all for admins, own for faculty, enrolled for students."""
    subjects = Subject.objects.select_related("course")
    if user.is_admin_user:
        return subjects
    if user.is_faculty:
        return subjects.filter(faculty__user=user)
    student = getattr(user, "student_profile", None)
    if student is None:
        return subjects.none()
    return subjects.filter(course=student.course, semester=student.semester)


def _parse_date(value, default):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return default


@login_required
def attendance_list(request):
    user = request.user
    records = Attendance.objects.select_related("student__user", "subject", "marked_by")
    if user.is_student:
        records = records.filter(student__user=user)
    elif user.is_faculty:
        records = records.filter(subject__faculty__user=user)

    form = AttendanceFilterForm(request.GET or None, subjects=subjects_for(user))
    if form.is_valid():
        if form.cleaned_data["subject"]:
            records = records.filter(subject=form.cleaned_data["subject"])
        if form.cleaned_data["date"]:
            records = records.filter(date=form.cleaned_data["date"])
        if form.cleaned_data["status"]:
            records = records.filter(status=form.cleaned_data["status"])

    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "form": form,
        "page_obj": Paginator(records, 25).get_page(request.GET.get("page")),
        "querystring": params.urlencode(),
    }
    return render(request, "attendance/attendance_list.html", context)


@staff_required
def attendance_mark(request):
    today = timezone.localdate()
    subjects = subjects_for(request.user)
    data = request.POST if request.method == "POST" else request.GET
    subject_id = data.get("subject")
    att_date = _parse_date(data.get("date"), today)
    if att_date > today:
        messages.warning(request, "Attendance cannot be marked for a future date.")
        att_date = today

    context = {"subjects": subjects, "att_date": att_date, "status_choices": Attendance.Status.choices}
    if subject_id:
        subject = get_object_or_404(subjects, pk=subject_id)
        students = Student.objects.filter(course=subject.course, semester=subject.semester).select_related("user")

        if request.method == "POST":
            valid_statuses = Attendance.Status.values
            saved = 0
            for student in students:
                status = request.POST.get(f"status_{student.pk}")
                if status in valid_statuses:
                    Attendance.objects.update_or_create(
                        student=student, subject=subject, date=att_date,
                        defaults={"status": status, "marked_by": request.user},
                    )
                    saved += 1
            messages.success(request, f"Attendance saved for {saved} student(s) in {subject.code} on {att_date}.")
            return redirect(f"{reverse('attendance:list')}?subject={subject.pk}&date={att_date.isoformat()}")

        existing = dict(Attendance.objects.filter(subject=subject, date=att_date).values_list("student_id", "status"))
        context.update({
            "subject": subject,
            "rows": [(s, existing.get(s.pk, Attendance.Status.PRESENT)) for s in students],
            "already_marked": bool(existing),
        })
    return render(request, "attendance/attendance_mark.html", context)


@login_required
def attendance_report(request):
    user = request.user
    threshold = settings.ATTENDANCE_THRESHOLD
    context = {"threshold": threshold}

    if user.is_student:
        student = getattr(user, "student_profile", None)
        if student:
            rows = [(s, student.attendance_summary(s)) for s in subjects_for(user)]
            context.update({"student": student, "student_rows": rows, "overall": student.attendance_summary()})
        return render(request, "attendance/attendance_report.html", context)

    subjects = subjects_for(user)
    context["subjects"] = subjects
    subject_id = request.GET.get("subject")
    if subject_id:
        subject = get_object_or_404(subjects, pk=subject_id)
        in_subject = Q(attendance_records__subject=subject)
        students = (
            Student.objects.filter(course=subject.course, semester=subject.semester)
            .select_related("user")
            .annotate(
                total=Count("attendance_records", filter=in_subject),
                present=Count(
                    "attendance_records",
                    filter=in_subject & Q(attendance_records__status__in=Attendance.PRESENT_STATUSES),
                ),
            )
        )
        rows = [
            {
                "student": s,
                "total": s.total,
                "present": s.present,
                "absent": s.total - s.present,
                "percentage": round(s.present * 100 / s.total, 1) if s.total else 0,
            }
            for s in students
        ]
        context.update({
            "subject": subject,
            "rows": rows,
            "classes_held": Attendance.objects.filter(subject=subject).values("date").distinct().count(),
            "shortage_count": sum(1 for r in rows if r["total"] and r["percentage"] < threshold),
        })
    return render(request, "attendance/attendance_report.html", context)
