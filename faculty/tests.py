from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from courses.models import Department

from .models import Faculty


class FacultyViewTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Physics", code="PHY")
        self.admin = User.objects.create_superuser("admin", "admin@x.com", "pass12345")

    def test_admin_can_add_faculty(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("faculty:add"), {
            "user-username": "drsharma", "user-first_name": "Anita", "user-last_name": "Sharma",
            "user-email": "anita@x.com", "user-phone": "", "user-password1": "Sup3r-Secret-Pass",
            "user-password2": "Sup3r-Secret-Pass",
            "faculty-employee_id": "EMP001", "faculty-department": self.dept.pk,
            "faculty-designation": "PROF", "faculty-date_of_joining": "2020-06-01",
        })
        member = Faculty.objects.get(employee_id="EMP001")
        self.assertRedirects(response, reverse("faculty:detail", args=[member.pk]))
        self.assertTrue(member.user.is_faculty)

    def test_faculty_cannot_manage_faculty(self):
        user = User.objects.create_user("f", password="x", role=User.Role.FACULTY)
        self.client.force_login(user)
        self.assertRedirects(self.client.get(reverse("faculty:list")), reverse("accounts:dashboard"))
