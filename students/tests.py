from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from courses.models import Course, Department

from .models import Student


class StudentViewTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name="Commerce", code="COM")
        self.course = Course.objects.create(name="B.Com", code="BCOM", department=dept)
        self.admin = User.objects.create_superuser("admin", "admin@x.com", "pass12345")

    def test_admin_can_add_student(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("students:add"), {
            "user-username": "ravi", "user-first_name": "Ravi", "user-last_name": "Kumar",
            "user-email": "ravi@x.com", "user-phone": "", "user-password1": "Sup3r-Secret-Pass",
            "user-password2": "Sup3r-Secret-Pass",
            "student-roll_number": "BCOM001", "student-course": self.course.pk, "student-semester": 1,
            "student-gender": "M", "student-admission_date": "2026-07-01",
        })
        student = Student.objects.get(roll_number="BCOM001")
        self.assertRedirects(response, reverse("students:detail", args=[student.pk]))
        self.assertEqual(student.user.role, User.Role.STUDENT)

    def test_student_cannot_view_other_student(self):
        a = Student.objects.create(user=User.objects.create_user("a", password="x"), roll_number="1", course=self.course)
        b = Student.objects.create(user=User.objects.create_user("b", password="x"), roll_number="2", course=self.course)
        self.client.force_login(a.user)
        self.assertEqual(self.client.get(reverse("students:detail", args=[a.pk])).status_code, 200)
        self.assertRedirects(self.client.get(reverse("students:detail", args=[b.pk])), reverse("accounts:dashboard"))

    def test_delete_removes_user(self):
        student = Student.objects.create(user=User.objects.create_user("c", password="x"), roll_number="3")
        self.client.force_login(self.admin)
        self.client.post(reverse("students:delete", args=[student.pk]))
        self.assertFalse(User.objects.filter(username="c").exists())
