from django.urls import path
from . import views

app_name = "cashflows"
urlpatterns = [
    path("", views.index, name="index"),
    path("request/", views.request_payment, name="request_payment"),
    path("payment/confirm", views.confirm, name="confirm"),
]
