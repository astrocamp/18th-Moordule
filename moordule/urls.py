from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("activities/", include("activities.urls")),
    path("cashflows/", include("cashflows.urls")),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),  # allauth URL
]
