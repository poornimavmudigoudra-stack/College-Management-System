from django import forms

from accounts.forms import BootstrapFormMixin, DateInput

from .models import Exam


class ExamForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["name", "exam_type", "subject", "date", "max_marks", "pass_marks"]
        widgets = {"date": DateInput()}

    def __init__(self, *args, subjects=None, **kwargs):
        super().__init__(*args, **kwargs)
        if subjects is not None:
            self.fields["subject"].queryset = subjects
