from django import forms

from accounts.forms import BootstrapFormMixin, DateInput
from courses.models import Course

from .models import Fee, Payment


class FeeForm(BootstrapFormMixin, forms.ModelForm):
    """Assign a fee to one student, or to every student of a course/semester at once."""

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), required=False,
        help_text="Leave the student empty and pick a course to assign this fee to all its students.",
    )
    semester = forms.IntegerField(required=False, min_value=1, max_value=12,
                                  help_text="Optional: only students of this semester.")

    class Meta:
        model = Fee
        fields = ["student", "course", "semester", "fee_type", "amount", "due_date", "description"]
        widgets = {"due_date": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].required = False
        self.fields["student"].queryset = self.fields["student"].queryset.select_related("user")

    def clean(self):
        cleaned = super().clean()
        student, course = cleaned.get("student"), cleaned.get("course")
        if not student and not course:
            raise forms.ValidationError("Choose a student or a course.")
        if student and course:
            raise forms.ValidationError("Choose either a single student or a course, not both.")
        return cleaned

    def target_students(self):
        if self.cleaned_data.get("student"):
            return [self.cleaned_data["student"]]
        students = self.cleaned_data["course"].students.all()
        if self.cleaned_data.get("semester"):
            students = students.filter(semester=self.cleaned_data["semester"])
        return list(students)


class PaymentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "payment_date", "method", "transaction_id", "remarks"]
        widgets = {"payment_date": DateInput()}

    def __init__(self, *args, fee, **kwargs):
        super().__init__(*args, **kwargs)
        self.fee = fee
        self.fields["amount"].initial = fee.balance
        self.fields["amount"].help_text = f"Outstanding balance: ₹{fee.balance}"

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount > self.fee.balance:
            raise forms.ValidationError(f"Amount exceeds the outstanding balance of ₹{self.fee.balance}.")
        return amount
