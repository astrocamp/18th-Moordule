from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from activities.models import Activity

# Create your views here.


def index_view(request):
    now = timezone.now()
    tomorrow = now + timedelta(days=1)

    upcoming_activities = Activity.objects.filter(
        start_time__gte=now, start_time__lte=tomorrow, status="approved"
    ).order_by("start_time")[:4]

    context = {
        "upcoming_activities": upcoming_activities,
    }

    return render(request, "pages/index.html", context)


def privacy(request):
    return render(request, "pages/privacy.html")
