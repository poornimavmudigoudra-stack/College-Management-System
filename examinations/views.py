from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Min
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from accounts.decorators import staff_required
from attendance.views import subjects_for
from students.models import Student

from .forms import ExamForm
from .models import Exam, Mark


@login_required
def exam_list(request):
    today = timezone.localdate()
    exams = (
        Exam.objects.filter(subject__in=subjects_for(request.user))
        .select_related("subject__course")
        .annotate(num_marks=Count("marks"))
    )
    show = request.GET.get("show", "all")
    if show == "upcoming":
        exams = exams.filter(date__gte=today)
    elif show == "past":
        exams = exams.filter(date__lt=today)
    return render(request, "examinations/exam_list.html", {"exams": exams, "show": show, "today": today})


@staff_required
def exam_add(request):
    subjects = subjects_for(request.user)
    form = ExamForm(request.POST or None, subjects=subjects)
    if request.method == "POST" and form.is_valid():
        exam = form.save(commit=False)
        exam.created_by = request.user
        exam.save()
        messages.success(request, f"Exam '{exam}' scheduled for {exam.date}.")
        return redirect("examinations:list")
    return render(request, "examinations/exam_add.html", {"form": form})


@staff_required
def marks_entry(request, pk):
    exam = get_object_or_404(
        Exam.objects.select_related("subject__course").filter(subject__in=subjects_for(request.user)), pk=pk
    )
    students = Student.objects.filter(course=exam.subject.course, semester=exam.subject.semester).select_related("user")
    existing = {m.student_id: m for m in exam.marks.all()}

    if request.method == "POST":
        saved, errors = 0, []
        for student in students:
            raw = request.POST.get(f"marks_{student.pk}", "").strip()
            if not raw:
                continue
            try:
                value = Decimal(raw)
            except InvalidOperation:
                errors.append(f"{student.roll_number}: '{raw}' is not a number.")
                continue
            if not 0 <= value <= exam.max_marks:
                errors.append(f"{student.roll_number}: marks must be between 0 and {exam.max_marks}.")
                continue
            Mark.objects.update_or_create(
                exam=exam, student=student,
                defaults={"marks_obtained": value, "remarks": request.POST.get(f"remarks_{student.pk}", "").strip()},
            )
            saved += 1
        for error in errors:
            messages.error(request, error)
        if saved:
            messages.success(request, f"Marks saved for {saved} student(s).")
        if errors:
            return redirect("examinations:marks_entry", pk=exam.pk)
        return redirect(f"{reverse('examinations:results')}?exam={exam.pk}")

    rows = [(s, existing.get(s.pk)) for s in students]
    return render(request, "examinations/marks_entry.html", {"exam": exam, "rows": rows})


@login_required
def results(request):
    user = request.user
    if user.is_student:
        student = getattr(user, "student_profile", None)
        marks = (
            Mark.objects.filter(student=student).select_related("exam__subject").order_by("-exam__date")
            if student else Mark.objects.none()
        )
        marks = list(marks)
        context = {
            "student": student,
            "marks": marks,
            "passed": sum(1 for m in marks if m.is_pass),
            "average": round(sum(m.percentage for m in marks) / len(marks), 1) if marks else 0,
        }
        return render(request, "examinations/results.html", context)

    exams = Exam.objects.filter(subject__in=subjects_for(user)).select_related("subject")
    context = {"exams": exams}
    exam_id = request.GET.get("exam")
    if exam_id:
        exam = get_object_or_404(exams, pk=exam_id)
        marks = list(exam.marks.select_related("student__user").order_by("-marks_obtained"))
        context.update({
            "exam": exam,
            "exam_marks": marks,
            "stats": exam.marks.aggregate(avg=Avg("marks_obtained"), high=Max("marks_obtained"), low=Min("marks_obtained")),
            "pass_count": sum(1 for m in marks if m.is_pass),
        })
    return render(request, "examinations/results.html", context)
