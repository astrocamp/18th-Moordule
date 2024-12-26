from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("signin/", views.signin_view, name="signin"),
    path("login/", views.login_view, name="login"),
    path("new/", views.user_create_view, name="new"),
    path("clear-errors/", views.clear_errors, name="clear_errors"),
    path("records/<str:tag>/", views.records_tag, name="records"),
    path("", views.dashboard_view, name="dashboard"),
    path("upload", views.upload_view, name="upload"),
    path("meetup/new", views.meetup_create_view, name="meetup_new"),
    # path("chat/<int:meetup_id>/", views.chat_room, name="chat_room"),
]
