from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Notice


class NoticeTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@x.com", "x")
        self.faculty = User.objects.create_user("f", password="x", role=User.Role.FACULTY)
        self.student = User.objects.create_user("s", password="x", role=User.Role.STUDENT)
        for audience in Notice.Audience.values:
            Notice.objects.create(title=audience, content="...", audience=audience, posted_by=self.admin)
        Notice.objects.create(title="hidden", content="...", is_active=False, posted_by=self.admin)

    def titles(self, user):
        return set(Notice.objects.for_user(user).values_list("title", flat=True))

    def test_visibility_by_role(self):
        self.assertEqual(self.titles(AnonymousUser()), {"ALL"})
        self.assertEqual(self.titles(self.student), {"ALL", "STUDENTS"})
        self.assertEqual(self.titles(self.faculty), {"ALL", "FACULTY"})
        self.assertEqual(self.titles(self.admin), {"ALL", "STUDENTS", "FACULTY"})

    def test_student_cannot_open_faculty_notice(self):
        notice = Notice.objects.get(title="FACULTY")
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse("notices:detail", args=[notice.pk])).status_code, 404)

    def test_faculty_can_post(self):
        self.client.force_login(self.faculty)
        self.client.post(reverse("notices:add"), {"title": "Lab closed", "audience": "STUDENTS", "content": "Friday"})
        self.assertEqual(Notice.objects.get(title="Lab closed").posted_by, self.faculty)
