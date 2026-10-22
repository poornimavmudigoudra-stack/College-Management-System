from django.contrib import admin

from .models import Fee, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ("receipt_number",)


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ("student", "fee_type", "amount", "due_date", "status")
    list_filter = ("fee_type", "due_date", "student__course")
    search_fields = ("student__roll_number", "student__user__first_name", "description")
    autocomplete_fields = ("student",)
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("receipt_number", "fee", "amount", "method", "payment_date", "received_by")
    list_filter = ("method", "payment_date")
    search_fields = ("receipt_number", "transaction_id", "fee__student__roll_number")
    readonly_fields = ("receipt_number",)
    date_hierarchy = "payment_date"
