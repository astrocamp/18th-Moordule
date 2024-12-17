from django.urls import path
from .views import index

app_name="cashflows"
urlpatterns = [
    path("",index,name="index")
]
