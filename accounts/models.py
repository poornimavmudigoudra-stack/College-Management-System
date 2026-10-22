from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with a role that drives what each person can see and do."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FACULTY = "FACULTY", "Faculty"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=15, blank=True)

    def save(self, *args, **kwargs):
        # Superusers created with `createsuperuser` should always act as admins
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    @property
    def is_admin_user(self):
        return self.is_superuser or self.role == self.Role.ADMIN

    @property
    def is_faculty(self):
        return self.role == self.Role.FACULTY

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return f"{self.display_name} ({self.get_role_display()})"
