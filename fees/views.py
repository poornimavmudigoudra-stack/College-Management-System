from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required

from .forms import FeeForm, PaymentForm
from .models import Fee, Payment


def _deny_faculty(request):
    messages.error(request, "Fee records are only available to administrators and students.")
    return redirect("accounts:dashboard")


@login_required
def fee_list(request):
    user = request.user
    if user.is_faculty:
        return _deny_faculty(request)

    fees = Fee.objects.select_related("student__user", "student__course")
    if user.is_student:
        fees = fees.filter(student__user=user)

    status = request.GET.get("status", "")
    fees = {"paid": fees.paid, "partial": fees.partial, "unpaid": fees.unpaid}.get(status, fees.with_paid_total)()
    q = request.GET.get("q", "").strip()
    if q and not user.is_student:
        fees = fees.filter(
            Q(student__roll_number__icontains=q)
            | Q(student__user__first_name__icontains=q)
            | Q(student__user__last_name__icontains=q)
        )

    total_amount = sum(f.amount for f in fees)
    total_paid = sum(f.paid_total for f in fees)
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "page_obj": Paginator(fees, 20).get_page(request.GET.get("page")),
        "status": status,
        "q": q,
        "total_amount": total_amount,
        "total_paid": total_paid,
        "total_due": total_amount - total_paid,
        "querystring": params.urlencode(),
    }
    return render(request, "fees/fee_list.html", context)


@admin_required
@transaction.atomic
def fee_add(request):
    form = FeeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        students = form.target_students()
        if not students:
            messages.warning(request, "No students matched the selected course/semester.")
        else:
            data = {k: form.cleaned_data[k] for k in ("fee_type", "amount", "due_date", "description")}
            Fee.objects.bulk_create([Fee(student=s, **data) for s in students])
            messages.success(request, f"Fee assigned to {len(students)} student(s).")
            return redirect("fees:list")
    return render(request, "fees/fee_add.html", {"form": form, "title": "Assign Fee"})


@admin_required
def payment_add(request, fee_id):
    fee = get_object_or_404(Fee.objects.select_related("student__user"), pk=fee_id)
    if fee.balance <= 0:
        messages.info(request, "This fee is already fully paid.")
        return redirect("fees:list")
    form = PaymentForm(request.POST or None, fee=fee)
    if request.method == "POST" and form.is_valid():
        payment = form.save(commit=False)
        payment.fee = fee
        payment.received_by = request.user
        payment.save()
        messages.success(request, f"Payment recorded. Receipt {payment.receipt_number}.")
        return redirect("fees:receipt", pk=payment.pk)
    context = {"form": form, "fee": fee, "title": f"Record Payment - {fee.student}"}
    return render(request, "fees/fee_add.html", context)


@login_required
def payment_history(request):
    user = request.user
    if user.is_faculty:
        return _deny_faculty(request)

    payments = Payment.objects.select_related("fee__student__user", "received_by")
    if user.is_student:
        payments = payments.filter(fee__student__user=user)
    q = request.GET.get("q", "").strip()
    if q and not user.is_student:
        payments = payments.filter(
            Q(receipt_number__icontains=q)
            | Q(fee__student__roll_number__icontains=q)
            | Q(fee__student__user__first_name__icontains=q)
            | Q(transaction_id__icontains=q)
        )
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "page_obj": Paginator(payments, 20).get_page(request.GET.get("page")),
        "total": payments.aggregate(total=Sum("amount"))["total"] or 0,
        "q": q,
        "querystring": params.urlencode(),
    }
    return render(request, "fees/payment_history.html", context)


@login_required
def fee_receipt(request, pk):
    payment = get_object_or_404(
        Payment.objects.select_related("fee__student__user", "fee__student__course", "received_by"), pk=pk
    )
    user = request.user
    if not (user.is_admin_user or payment.fee.student.user_id == user.id):
        messages.error(request, "You cannot view this receipt.")
        return redirect("accounts:dashboard")
    return render(request, "fees/fee_receipt.html", {"payment": payment, "fee": payment.fee})
