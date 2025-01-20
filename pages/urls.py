from django.urls import path

from . import views

app_name = "pages"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("info", views.info, name="info"),
    path("privacy", views.privacy, name="privacy"),
    path("service_terms", views.service_terms, name="service_terms"),
]
