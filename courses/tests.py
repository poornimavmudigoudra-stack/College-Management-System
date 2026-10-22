from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .forms import SubjectForm
from .models import Course, Department


class CourseTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Computer Science", code="CS")
        self.course = Course.objects.create(name="BCA", code="BCA", department=self.dept, duration_years=3)

    def test_total_semesters(self):
        self.assertEqual(self.course.total_semesters, 6)

    def test_subject_semester_cannot_exceed_course_length(self):
        form = SubjectForm(data={"name": "AI", "code": "AI1", "course": self.course.pk, "semester": 7, "credits": 4})
        self.assertFalse(form.is_valid())
        self.assertIn("semester", form.errors)

    def test_students_cannot_view_courses(self):
        self.client.force_login(User.objects.create_user("s", password="x", role=User.Role.STUDENT))
        self.assertRedirects(self.client.get(reverse("courses:list")), reverse("accounts:dashboard"))

    def test_admin_can_add_course(self):
        self.client.force_login(User.objects.create_superuser("a", "a@x.com", "x"))
        response = self.client.post(reverse("courses:add"), {
            "name": "MCA", "code": "MCA", "department": self.dept.pk, "duration_years": 2, "description": "",
        })
        course = Course.objects.get(code="MCA")
        self.assertRedirects(response, reverse("courses:detail", args=[course.pk]))
