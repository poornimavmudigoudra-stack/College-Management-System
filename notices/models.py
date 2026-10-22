from django.conf import settings
from django.db import models


class NoticeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def for_user(self, user):
        """Active notices the given user (or an anonymous visitor) is allowed to see."""
        notices = self.active()
        if not user.is_authenticated:
            return notices.filter(audience=Notice.Audience.ALL)
        if user.is_admin_user:
            return notices
        if user.is_faculty:
            return notices.filter(audience__in=[Notice.Audience.ALL, Notice.Audience.FACULTY])
        return notices.filter(audience__in=[Notice.Audience.ALL, Notice.Audience.STUDENTS])


class Notice(models.Model):
    class Audience(models.TextChoices):
        ALL = "ALL", "Everyone"
        STUDENTS = "STUDENTS", "Students"
        FACULTY = "FACULTY", "Faculty"

    title = models.CharField(max_length=200)
    content = models.TextField()
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.ALL)
    is_important = models.BooleanField(default=False, help_text="Important notices are highlighted.")
    is_active = models.BooleanField(default=True, help_text="Inactive notices are hidden from everyone but admins in the admin site.")
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="notices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NoticeQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
