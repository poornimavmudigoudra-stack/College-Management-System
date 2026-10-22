from django import forms

from accounts.forms import BootstrapFormMixin

from .models import Notice


class NoticeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Notice
        fields = ["title", "audience", "content", "is_important"]
        widgets = {"content": forms.Textarea(attrs={"rows": 8})}
