from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("activities/", include("activities.urls")),
    path("cashflows/", include("cashflows.urls")),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),  # allauth URL
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
