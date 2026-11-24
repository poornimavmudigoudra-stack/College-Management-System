from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required, staff_required
from accounts.forms import UserCreateForm, UserUpdateForm
from accounts.models import User
from courses.models import Course, Subject
from examinations.models import Mark
from fees.models import Fee

from .forms import StudentForm
from .models import Student


@staff_required
def student_list(request):
    students = Student.objects.select_related("user", "course")
    q = request.GET.get("q", "").strip()
    if q:
        students = students.filter(
            Q(roll_number__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(user__email__icontains=q)
        )
    course_id = request.GET.get("course")
    if course_id:
        students = students.filter(course_id=course_id)
    semester = request.GET.get("semester")
    if semester:
        students = students.filter(semester=semester)

    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "page_obj": Paginator(students, 15).get_page(request.GET.get("page")),
        "courses": Course.objects.all(),
        "q": q,
        "selected_course": course_id,
        "selected_semester": semester,
        "semesters": range(1, 9),
        "querystring": params.urlencode(),
    }
    return render(request, "students/student_list.html", context)


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related("user", "course__department"), pk=pk)
    user = request.user
    if not (user.is_admin_user or user.is_faculty or student.user_id == user.id):
        messages.error(request, "You can only view your own profile.")
        return redirect("accounts:dashboard")

    subjects = Subject.objects.filter(course=student.course, semester=student.semester)
    context = {
        "student": student,
        "threshold": settings.ATTENDANCE_THRESHOLD,
        "attendance": student.attendance_summary(),
        "subject_attendance": [(s, student.attendance_summary(s)) for s in subjects],
        "marks": Mark.objects.filter(student=student).select_related("exam__subject").order_by("-exam__date")[:10],
        "fees": Fee.objects.filter(student=student).with_paid_total().order_by("-due_date"),
    }
    return render(request, "students/student_detail.html", context)


@admin_required
@transaction.atomic
def student_add(request):
    user_form = UserCreateForm(request.POST or None, prefix="user")
    student_form = StudentForm(request.POST or None, request.FILES or None, prefix="student")
    if request.method == "POST" and all([user_form.is_valid(), student_form.is_valid()]):
        user = user_form.save(commit=False)
        user.role = User.Role.STUDENT
        user.save()
        student = student_form.save(commit=False)
        student.user = user
        student.save()
        messages.success(request, f"Student {student.full_name} added successfully.")
        return redirect("students:detail", pk=student.pk)
    return render(request, "students/student_add.html", {"user_form": user_form, "student_form": student_form})


@admin_required
@transaction.atomic
def student_edit(request, pk):
    student = get_object_or_404(Student.objects.select_related("user"), pk=pk)
    user_form = UserUpdateForm(request.POST or None, instance=student.user, prefix="user")
    student_form = StudentForm(request.POST or None, request.FILES or None, instance=student, prefix="student")
    if request.method == "POST" and all([user_form.is_valid(), student_form.is_valid()]):
        user_form.save()
        student_form.save()
        messages.success(request, "Student details updated.")
        return redirect("students:detail", pk=student.pk)
    context = {"user_form": user_form, "student_form": student_form, "student": student}
    return render(request, "students/student_edit.html", context)


@admin_required
def student_delete(request, pk):
    student = get_object_or_404(Student.objects.select_related("user"), pk=pk)
    if request.method == "POST":
        name = student.full_name
        student.user.delete()  # cascades to the student record
        messages.success(request, f"Student {name} deleted.")
        return redirect("students:list")
    return render(request, "students/student_delete.html", {"student": student})
