from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "users"


frontend = [
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
]

backend = [
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("login/", views.login_view, name="login"),
    path("password-change/", views.password_change_view, name="password_change"),
]

htmx = [
    path("", views.user_page_view, {"tag": "member"}, name="account"),
    path("new/", views.user_create_view, name="new"),
    path("edit/", views.edit_view, name="edit"),
    path("clear-errors/", views.clear_errors, name="clear_errors"),
    path("<str:tag>/", views.user_page_view, name="user_page"),
]

urlpatterns = frontend + backend + htmx
