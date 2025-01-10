from django.urls import path, re_path
from . import views

app_name = "users"


frontend = [
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
]

backend = [
    path("logout/", views.CustomLogoutView.as_view(next_page="/"), name="logout"),
    path("login/", views.login_view, name="login"),
    path("password-change/", views.password_change_view, name="password_change"),
    path("info/edit", views.info_edit_view, name="info_edit"),
    path("upload", views.upload_view, name="upload"),
]

htmx = [
    path("", views.user_page_view, {"tag": "member"}, name="account"),
    path("new/", views.user_create_view, name="new"),
    path("clear-errors/", views.clear_errors, name="clear_errors"),
    path("info/", views.info_view, name="info"),
    path("info_form/", views.info_form_view, name="info_form"),
    path("password/", views.password_view, name="password"),
    path("about_me/", views.about_me_view, name="about_me"),
    path("about_me/edit/", views.about_me_edit_view, name="about_me_edit"),
    re_path(
        r"^(?P<tag>member|account|activities|my_activities)/?$",  # 修改使用正規表達式使用tag
        views.user_page_view,
        name="user_page",
    ),
]

urlpatterns = frontend + backend + htmx
