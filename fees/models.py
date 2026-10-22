from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import DecimalField, F, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone


class FeeQuerySet(models.QuerySet):
    def with_paid_total(self):
        return self.annotate(
            paid_total=Coalesce(
                Sum("payments__amount"), Value(Decimal("0")),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )

    def paid(self):
        return self.with_paid_total().filter(paid_total__gte=F("amount"))

    def partial(self):
        return self.with_paid_total().filter(paid_total__gt=0, paid_total__lt=F("amount"))

    def unpaid(self):
        return self.with_paid_total().filter(paid_total=0)


class Fee(models.Model):
    class FeeType(models.TextChoices):
        TUITION = "TUITION", "Tuition Fee"
        EXAM = "EXAM", "Examination Fee"
        LIBRARY = "LIBRARY", "Library Fee"
        HOSTEL = "HOSTEL", "Hostel Fee"
        TRANSPORT = "TRANSPORT", "Transport Fee"
        OTHER = "OTHER", "Other"

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="fees")
    fee_type = models.CharField(max_length=10, choices=FeeType.choices, default=FeeType.TUITION)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("1"))])
    due_date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FeeQuerySet.as_manager()

    class Meta:
        ordering = ["-due_date"]

    def __str__(self):
        return f"{self.get_fee_type_display()} - {self.student.roll_number} (₹{self.amount})"

    @property
    def paid_amount(self):
        # Use the annotated total when available to avoid an extra query per row
        if hasattr(self, "paid_total"):
            return self.paid_total
        return self.payments.aggregate(total=Sum("amount"))["total"] or Decimal("0")

    @property
    def balance(self):
        return self.amount - self.paid_amount

    @property
    def status(self):
        paid = self.paid_amount
        if paid >= self.amount:
            return "Paid"
        return "Partial" if paid > 0 else "Unpaid"

    @property
    def is_overdue(self):
        return self.balance > 0 and self.due_date < timezone.localdate()


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "CASH", "Cash"
        CARD = "CARD", "Card"
        UPI = "UPI", "UPI"
        BANK = "BANK", "Bank Transfer"
        CHEQUE = "CHEQUE", "Cheque"

    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("1"))])
    payment_date = models.DateField(default=timezone.localdate)
    method = models.CharField(max_length=10, choices=Method.choices, default=Method.CASH)
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_number = models.CharField(max_length=30, unique=True, editable=False)
    remarks = models.CharField(max_length=200, blank=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date", "-id"]

    def __str__(self):
        return f"{self.receipt_number} - ₹{self.amount}"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = self._next_receipt_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _next_receipt_number():
        """Receipt numbers look like RCPT-2026-00001 and restart every year."""
        prefix = f"RCPT-{timezone.localdate().year}-"
        last = Payment.objects.filter(receipt_number__startswith=prefix).order_by("-receipt_number").first()
        next_no = int(last.receipt_number.rsplit("-", 1)[1]) + 1 if last else 1
        return f"{prefix}{next_no:05d}"
