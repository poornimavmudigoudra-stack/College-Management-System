from django.conf import settings
from django.db import models
from django.utils import timezone


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey("courses.Course", on_delete=models.SET_NULL, null=True, related_name="students")
    semester = models.PositiveSmallIntegerField(default=1)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    admission_date = models.DateField(default=timezone.localdate)
    photo = models.ImageField(upload_to="student_photos/", blank=True)

    class Meta:
        ordering = ["roll_number"]

    def __str__(self):
        return f"{self.roll_number} - {self.full_name}"

    @property
    def full_name(self):
        return self.user.display_name

    def attendance_summary(self, subject=None):
        """Totals and percentage of classes attended (late counts as present)."""
        from attendance.models import Attendance

        records = self.attendance_records.all()
        if subject is not None:
            records = records.filter(subject=subject)
        total = records.count()
        present = records.filter(status__in=Attendance.PRESENT_STATUSES).count()
        return {
            "total": total,
            "present": present,
            "absent": total - present,
            "percentage": round(present * 100 / total, 1) if total else 0,
        }
