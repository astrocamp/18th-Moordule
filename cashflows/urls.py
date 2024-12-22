from django.urls import path
from .views import index,request_payment

app_name="cashflows"
urlpatterns = [
    path("",index,name="index"),
    path('request/', request_payment, name='request_payment'),
]
