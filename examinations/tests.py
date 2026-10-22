from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from courses.models import Course, Department, Subject
from students.models import Student

from .models import Exam, Mark


class ExaminationTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name="Mathematics", code="MAT")
        course = Course.objects.create(name="B.Sc", code="BSC", department=dept)
        subject = Subject.objects.create(name="Algebra", code="ALG1", course=course, semester=1)
        self.exam = Exam.objects.create(name="Internal 1", subject=subject, date=timezone.localdate(),
                                        max_marks=50, pass_marks=20)
        self.student = Student.objects.create(user=User.objects.create_user("s", password="x"),
                                              roll_number="R1", course=course)
        self.admin = User.objects.create_superuser("admin", "a@x.com", "x")

    def test_grade_calculation(self):
        mark = Mark(exam=self.exam, student=self.student, marks_obtained=Decimal("46"))
        self.assertEqual(mark.percentage, 92.0)
        self.assertEqual(mark.grade, "O")
        mark.marks_obtained = Decimal("15")
        self.assertEqual(mark.grade, "F")

    def test_marks_entry_saves_and_rejects_out_of_range(self):
        self.client.force_login(self.admin)
        url = reverse("examinations:marks_entry", args=[self.exam.pk])
        self.client.post(url, {f"marks_{self.student.pk}": "60"})
        self.assertFalse(Mark.objects.exists())
        self.client.post(url, {f"marks_{self.student.pk}": "42.5"})
        self.assertEqual(Mark.objects.get().marks_obtained, Decimal("42.5"))

    def test_student_sees_own_results(self):
        Mark.objects.create(exam=self.exam, student=self.student, marks_obtained=30)
        self.client.force_login(self.student.user)
        response = self.client.get(reverse("examinations:results"))
        self.assertEqual(len(response.context["marks"]), 1)
