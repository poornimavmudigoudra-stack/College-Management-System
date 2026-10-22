from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from courses.models import Course, Department, Subject
from faculty.models import Faculty
from students.models import Student

from .models import Attendance


class AttendanceTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name="Computer Science", code="CS")
        course = Course.objects.create(name="BCA", code="BCA", department=dept)
        self.teacher = User.objects.create_user("teacher", password="x", role=User.Role.FACULTY)
        faculty = Faculty.objects.create(user=self.teacher, employee_id="E1", department=dept)
        self.subject = Subject.objects.create(name="Python", code="PY101", course=course, semester=1, faculty=faculty)
        self.s1 = Student.objects.create(user=User.objects.create_user("s1", password="x"), roll_number="R1", course=course)
        self.s2 = Student.objects.create(user=User.objects.create_user("s2", password="x"), roll_number="R2", course=course)

    def test_faculty_marks_attendance(self):
        self.client.force_login(self.teacher)
        today = timezone.localdate().isoformat()
        self.client.post(reverse("attendance:mark"), {
            "subject": self.subject.pk, "date": today,
            f"status_{self.s1.pk}": "P", f"status_{self.s2.pk}": "A",
        })
        self.assertEqual(Attendance.objects.count(), 2)
        self.assertEqual(self.s1.attendance_summary()["percentage"], 100)
        self.assertEqual(self.s2.attendance_summary()["percentage"], 0)

    def test_remarking_updates_instead_of_duplicating(self):
        self.client.force_login(self.teacher)
        for status in ("A", "P"):
            self.client.post(reverse("attendance:mark"), {"subject": self.subject.pk, f"status_{self.s1.pk}": status})
        self.assertEqual(Attendance.objects.get(student=self.s1).status, "P")

    def test_late_counts_as_present(self):
        today = timezone.localdate()
        Attendance.objects.create(student=self.s1, subject=self.subject, date=today, status="L")
        Attendance.objects.create(student=self.s1, subject=self.subject, date=today - timedelta(days=1), status="A")
        self.assertEqual(self.s1.attendance_summary()["percentage"], 50)

    def test_students_cannot_mark(self):
        self.client.force_login(self.s1.user)
        self.assertRedirects(self.client.get(reverse("attendance:mark")), reverse("accounts:dashboard"))
