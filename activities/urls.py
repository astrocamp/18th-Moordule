from django.urls import path

from . import views

app_name = "activities"

urlpatterns = [
    path("", views.activities, name="index"),
    path("create/", views.create, name="create"),
    path("my_activities/", views.created_activities, name="my_activities"),
    path("<int:activity_id>/update/", views.update, name="update"),
    path("<int:activity_id>/delete/", views.delete, name="delete"),
    path(
        "<int:activity_id>/confirm_delete/", views.confirm_delete, name="confirm_delete"
    ),
    path("<int:activity_id>/join/", views.join_activity, name="join"),
    path("create_category/", views.create_category, name="category"),
    path(
        "<int:category_id>/category_delete/",
        views.delete_category,
        name="delete_category",
    ),
    path("search/", views.search, name="search"),
    path("eating/", views.eating, name="eating"),
    path("driking/", views.driking, name="driking"),
    path("sports/", views.sports, name="sports"),
    path("singing/", views.singing, name="singing"),
    path("movies/", views.movies, name="movies"),
    path("discussion/", views.discussion, name="discussion"),
]
