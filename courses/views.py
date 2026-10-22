from itertools import groupby

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.decorators import admin_required, staff_required

from .forms import CourseForm, DepartmentForm, SubjectForm
from .models import Course, Department, Subject


@staff_required
def course_list(request):
    courses = Course.objects.select_related("department").annotate(
        num_subjects=Count("subjects", distinct=True),
        num_students=Count("students", distinct=True),
    )
    department_id = request.GET.get("department")
    if department_id:
        courses = courses.filter(department_id=department_id)
    context = {
        "courses": courses,
        "departments": Department.objects.annotate(num_courses=Count("courses")),
        "selected_department": department_id,
    }
    return render(request, "courses/course_list.html", context)


@staff_required
def course_detail(request, pk):
    course = get_object_or_404(Course.objects.select_related("department"), pk=pk)
    subjects = course.subjects.select_related("faculty__user").order_by("semester", "code")
    context = {
        "course": course,
        "subjects_by_semester": [(sem, list(items)) for sem, items in groupby(subjects, key=lambda s: s.semester)],
        "student_count": course.students.count(),
    }
    return render(request, "courses/course_detail.html", context)


def _course_url(course_id):
    return reverse("courses:detail", args=[course_id])


def _save_form(request, form_class, template, title, instance=None, initial=None, success_url=None):
    """Shared create/update flow for the small course-related forms."""
    form = form_class(request.POST or None, instance=instance, initial=initial)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        messages.success(request, f"{obj} saved successfully.")
        return redirect(success_url(obj) if success_url else "courses:list")
    return render(request, template, {"form": form, "title": title, "object": instance})


@admin_required
def course_add(request):
    return _save_form(request, CourseForm, "courses/course_add.html", "Add Course",
                      success_url=lambda c: _course_url(c.pk))


@admin_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return _save_form(request, CourseForm, "courses/course_edit.html", f"Edit {course.code}",
                      instance=course, success_url=lambda c: _course_url(c.pk))


@admin_required
def department_add(request):
    return _save_form(request, DepartmentForm, "courses/course_add.html", "Add Department")


@admin_required
def subject_add(request):
    course_id = request.GET.get("course")
    return _save_form(request, SubjectForm, "courses/course_add.html", "Add Subject",
                      initial={"course": course_id} if course_id else None,
                      success_url=lambda s: _course_url(s.course_id))


@admin_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return _save_form(request, SubjectForm, "courses/course_edit.html", f"Edit {subject.code}",
                      instance=subject, success_url=lambda s: _course_url(s.course_id))
