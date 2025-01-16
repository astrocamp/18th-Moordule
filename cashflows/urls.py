from django.urls import path
from . import views

app_name = "cashflows"
urlpatterns = [
    path("", views.index, name="index"),
    path("request_b/", views.request_payment_b, name="request_payment_b"),
    path("request_a/", views.request_payment_a, name="request_payment_a"),
    path("request_c/", views.request_payment_c, name="request_payment_c"),
    path("payment/confirm_a", views.confirm_a, name="confirm_a"),
    path("payment/confirm_b", views.confirm_b, name="confirm_b"),
    path("payment/confirm_c", views.confirm_c, name="confirm_c"),
]
