from django.conf import settings
from django.db import models
from django.utils import timezone


class Faculty(models.Model):
    class Designation(models.TextChoices):
        PROFESSOR = "PROF", "Professor"
        ASSOCIATE = "ASSOC", "Associate Professor"
        ASSISTANT = "ASST", "Assistant Professor"
        LECTURER = "LECT", "Lecturer"
        LAB = "LAB", "Lab Instructor"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="faculty_profile")
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey("courses.Department", on_delete=models.SET_NULL, null=True, related_name="faculty")
    designation = models.CharField(max_length=10, choices=Designation.choices, default=Designation.ASSISTANT)
    qualification = models.CharField(max_length=150, blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_joining = models.DateField(default=timezone.localdate)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to="faculty_photos/", blank=True)

    class Meta:
        ordering = ["employee_id"]
        verbose_name_plural = "faculty"

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    @property
    def full_name(self):
        return self.user.display_name
