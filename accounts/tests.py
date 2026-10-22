from django.test import TestCase
from django.urls import reverse

from .models import User


class UserModelTests(TestCase):
    def test_superuser_is_admin(self):
        user = User.objects.create_superuser("root", "root@example.com", "pass12345")
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertTrue(user.is_admin_user)

    def test_default_role_is_student(self):
        user = User.objects.create_user("stud", password="pass12345")
        self.assertTrue(user.is_student)


class AuthViewTests(TestCase):
    def test_register_creates_student_and_logs_in(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newstudent",
            "first_name": "New",
            "last_name": "Student",
            "email": "new@example.com",
            "phone": "",
            "password1": "Sup3r-Secret-Pass",
            "password2": "Sup3r-Secret-Pass",
        })
        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertEqual(User.objects.get(username="newstudent").role, User.Role.STUDENT)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("accounts:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_each_role_sees_its_dashboard(self):
        for role, template in (
            (User.Role.ADMIN, "dashboard/admin_dashboard.html"),
            (User.Role.FACULTY, "dashboard/faculty_dashboard.html"),
            (User.Role.STUDENT, "dashboard/student_dashboard.html"),
        ):
            user = User.objects.create_user(f"u_{role}", password="pass12345", role=role)
            self.client.force_login(user)
            self.assertTemplateUsed(self.client.get(reverse("accounts:dashboard")), template)

    def test_home_page(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
