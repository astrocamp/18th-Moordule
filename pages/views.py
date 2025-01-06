from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from activities.views import activities
from activities.models import Activity

# Create your views here.


def index_view(request):
    now = timezone.now()
    tomorrow = now + timedelta(days=1)

    upcoming_activities = Activity.objects.filter(
        start_time__gte=now, start_time__lte=tomorrow
    ).order_by("start_time")

    context = {
        "upcoming_activities": upcoming_activities,
    }

    activities_context = activities(request)

    if isinstance(activities_context, dict):
        context.update(activities_context)
    else:
        print(f"activities(request) 返回的結果不是字典，而是：{activities_context}")

    return render(request, "pages/index.html", context)
