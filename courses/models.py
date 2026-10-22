from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="courses")
    duration_years = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(6)])
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def total_semesters(self):
        return self.duration_years * 2


class Subject(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subjects")
    semester = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    credits = models.PositiveSmallIntegerField(default=4)
    faculty = models.ForeignKey(
        "faculty.Faculty", on_delete=models.SET_NULL, null=True, blank=True, related_name="subjects"
    )

    class Meta:
        ordering = ["course", "semester", "code"]

    def __str__(self):
        return f"{self.code} - {self.name}"
