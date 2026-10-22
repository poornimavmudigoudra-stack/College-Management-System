from django.urls import path

from . import views

app_name = "fees"

urlpatterns = [
    path("", views.fee_list, name="list"),
    path("add/", views.fee_add, name="add"),
    path("<int:fee_id>/pay/", views.payment_add, name="payment_add"),
    path("payments/", views.payment_history, name="payments"),
    path("receipt/<int:pk>/", views.fee_receipt, name="receipt"),
]
