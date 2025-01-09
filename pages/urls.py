from django.urls import path

from . import views

app_name = "pages"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("privacy", views.privacy, name="privacy"),
    # path("", views.index_view, name="index"),
]
