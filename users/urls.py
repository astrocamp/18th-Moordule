from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.account_view, name="account"),
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
    path("login/", views.login_view, name="login"),
    path("edit/", views.edit_view, name="edit"),
    path("new/", views.user_create_view, name="new"),
    path("clear-errors/", views.clear_errors, name="clear_errors"),
    
]
