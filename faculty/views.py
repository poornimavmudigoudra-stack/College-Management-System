from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import admin_required
from accounts.forms import UserCreateForm, UserUpdateForm
from accounts.models import User
from courses.models import Department

from .forms import FacultyForm
from .models import Faculty


@admin_required
def faculty_list(request):
    faculty = Faculty.objects.select_related("user", "department").annotate(num_subjects=Count("subjects"))
    q = request.GET.get("q", "").strip()
    if q:
        faculty = faculty.filter(
            Q(employee_id__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(specialization__icontains=q)
        )
    department_id = request.GET.get("department")
    if department_id:
        faculty = faculty.filter(department_id=department_id)

    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "page_obj": Paginator(faculty, 15).get_page(request.GET.get("page")),
        "departments": Department.objects.all(),
        "q": q,
        "selected_department": department_id,
        "querystring": params.urlencode(),
    }
    return render(request, "faculty/faculty_list.html", context)


@admin_required
def faculty_detail(request, pk):
    member = get_object_or_404(Faculty.objects.select_related("user", "department"), pk=pk)
    context = {"member": member, "subjects": member.subjects.select_related("course")}
    return render(request, "faculty/faculty_detail.html", context)


@admin_required
@transaction.atomic
def faculty_add(request):
    user_form = UserCreateForm(request.POST or None, prefix="user")
    faculty_form = FacultyForm(request.POST or None, request.FILES or None, prefix="faculty")
    if request.method == "POST" and all([user_form.is_valid(), faculty_form.is_valid()]):
        user = user_form.save(commit=False)
        user.role = User.Role.FACULTY
        user.save()
        member = faculty_form.save(commit=False)
        member.user = user
        member.save()
        messages.success(request, f"Faculty member {member.full_name} added successfully.")
        return redirect("faculty:detail", pk=member.pk)
    return render(request, "faculty/faculty_add.html", {"user_form": user_form, "faculty_form": faculty_form})


@admin_required
@transaction.atomic
def faculty_edit(request, pk):
    member = get_object_or_404(Faculty.objects.select_related("user"), pk=pk)
    user_form = UserUpdateForm(request.POST or None, instance=member.user, prefix="user")
    faculty_form = FacultyForm(request.POST or None, request.FILES or None, instance=member, prefix="faculty")
    if request.method == "POST" and all([user_form.is_valid(), faculty_form.is_valid()]):
        user_form.save()
        faculty_form.save()
        messages.success(request, "Faculty details updated.")
        return redirect("faculty:detail", pk=member.pk)
    context = {"user_form": user_form, "faculty_form": faculty_form, "member": member}
    return render(request, "faculty/faculty_edit.html", context)


@admin_required
@require_POST
def faculty_delete(request, pk):
    member = get_object_or_404(Faculty.objects.select_related("user"), pk=pk)
    name = member.full_name
    member.user.delete()  # cascades to the faculty record; their subjects become unassigned
    messages.success(request, f"Faculty member {name} deleted.")
    return redirect("faculty:list")
