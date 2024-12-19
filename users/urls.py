from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("<int:id>/", views.dashboard_view, name="dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
    path("login/", views.login_view, name="login"),
    path("new/", views.user_create_view, name="new"),
    path("clear-errors/", views.clear_errors, name="clear_errors"),
]
