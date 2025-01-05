from django.db.models import Count
from django.utils import timezone

from activities.models import MeetupPaticipat


class UpcomingMeetupParticipant(MeetupPaticipat):
    class Meta:
        proxy = True
        app_label = "users"

    @classmethod
    def list(cls, user):
        return (
            cls.objects.filter(
                participant=user, activity__start_time__gt=timezone.now()
            )
            .annotate(total_count=Count("activity__participants"))
            .order_by("activity__start_time")
        )
