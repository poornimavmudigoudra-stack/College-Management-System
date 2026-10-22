from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from courses.models import Course, Department
from students.models import Student

from .models import Fee, Payment


class FeeTests(TestCase):
    def setUp(self):
        dept = Department.objects.create(name="Commerce", code="COM")
        self.course = Course.objects.create(name="B.Com", code="BCOM", department=dept)
        self.student = Student.objects.create(user=User.objects.create_user("s", password="x"),
                                              roll_number="R1", course=self.course)
        self.fee = Fee.objects.create(student=self.student, amount=Decimal("10000"),
                                      due_date=timezone.localdate() - timedelta(days=1))
        self.admin = User.objects.create_superuser("admin", "a@x.com", "x")

    def test_status_and_balance(self):
        self.assertEqual(self.fee.status, "Unpaid")
        self.assertTrue(self.fee.is_overdue)
        Payment.objects.create(fee=self.fee, amount=Decimal("4000"))
        self.assertEqual(self.fee.status, "Partial")
        self.assertEqual(self.fee.balance, Decimal("6000"))
        self.assertEqual(Fee.objects.partial().count(), 1)

    def test_receipt_numbers_increment(self):
        first = Payment.objects.create(fee=self.fee, amount=Decimal("100"))
        second = Payment.objects.create(fee=self.fee, amount=Decimal("100"))
        self.assertTrue(first.receipt_number.endswith("00001"))
        self.assertTrue(second.receipt_number.endswith("00002"))

    def test_overpayment_rejected(self):
        self.client.force_login(self.admin)
        self.client.post(reverse("fees:payment_add", args=[self.fee.pk]), {
            "amount": "20000", "payment_date": timezone.localdate().isoformat(), "method": "CASH",
        })
        self.assertFalse(Payment.objects.exists())

    def test_bulk_assign_to_course(self):
        Student.objects.create(user=User.objects.create_user("s2", password="x"), roll_number="R2", course=self.course)
        self.client.force_login(self.admin)
        self.client.post(reverse("fees:add"), {
            "course": self.course.pk, "fee_type": "EXAM", "amount": "500",
            "due_date": timezone.localdate().isoformat(),
        })
        self.assertEqual(Fee.objects.filter(fee_type="EXAM").count(), 2)

    def test_student_cannot_view_others_receipt(self):
        payment = Payment.objects.create(fee=self.fee, amount=Decimal("100"))
        other = User.objects.create_user("other", password="x")
        self.client.force_login(other)
        self.assertRedirects(self.client.get(reverse("fees:receipt", args=[payment.pk])), reverse("accounts:dashboard"))
