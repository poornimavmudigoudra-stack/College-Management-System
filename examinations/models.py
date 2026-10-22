from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Exam(models.Model):
    class ExamType(models.TextChoices):
        INTERNAL = "INT", "Internal Assessment"
        MIDTERM = "MID", "Mid Term"
        FINAL = "FIN", "Final / Semester End"
        PRACTICAL = "PRA", "Practical"

    name = models.CharField(max_length=150)
    exam_type = models.CharField(max_length=3, choices=ExamType.choices, default=ExamType.INTERNAL)
    subject = models.ForeignKey("courses.Subject", on_delete=models.CASCADE, related_name="exams")
    date = models.DateField()
    max_marks = models.PositiveSmallIntegerField(default=100)
    pass_marks = models.PositiveSmallIntegerField(default=35)
    created_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-date", "subject"]

    def __str__(self):
        return f"{self.name} - {self.subject.code}"

    def clean(self):
        if self.pass_marks > self.max_marks:
            raise ValidationError({"pass_marks": "Pass marks cannot be greater than maximum marks."})


class Mark(models.Model):
    GRADE_SCALE = ((90, "O"), (80, "A+"), (70, "A"), (60, "B+"), (50, "B"), (40, "C"))

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="marks")
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="marks")
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["exam", "student"]
        constraints = [models.UniqueConstraint(fields=["exam", "student"], name="unique_mark_per_exam")]

    def __str__(self):
        return f"{self.student.roll_number} - {self.exam}: {self.marks_obtained}"

    def clean(self):
        if self.marks_obtained is not None and self.exam_id and self.marks_obtained > self.exam.max_marks:
            raise ValidationError({"marks_obtained": f"Marks cannot exceed {self.exam.max_marks}."})

    @property
    def percentage(self):
        return round(float(self.marks_obtained) * 100 / self.exam.max_marks, 1) if self.exam.max_marks else 0

    @property
    def is_pass(self):
        return self.marks_obtained >= self.exam.pass_marks

    @property
    def grade(self):
        if not self.is_pass:
            return "F"
        for threshold, grade in self.GRADE_SCALE:
            if self.percentage >= threshold:
                return grade
        return "P"
