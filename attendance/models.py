from django.conf import settings
from django.db import models
from django.utils import timezone


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "P", "Present"
        ABSENT = "A", "Absent"
        LATE = "L", "Late"

    # Statuses that count towards a student's attendance percentage
    PRESENT_STATUSES = (Status.PRESENT, Status.LATE)

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="attendance_records")
    subject = models.ForeignKey("courses.Subject", on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PRESENT)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "subject", "student"]
        constraints = [
            models.UniqueConstraint(fields=["student", "subject", "date"], name="unique_attendance_per_day"),
        ]
        verbose_name_plural = "attendance"

    def __str__(self):
        return f"{self.student.roll_number} | {self.subject.code} | {self.date} | {self.get_status_display()}"
