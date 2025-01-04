from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from django_google_maps import fields as map_fields
   
class Category(models.Model):
    name = models.CharField(max_length=15, help_text="分類名稱")
    description = models.TextField(help_text="分類描述", blank=True, null=True)
    order = models.PositiveIntegerField(help_text="排序", default=0)

    def __str__(self):
        return self.name

class Activity(models.Model):
    title = models.CharField(max_length=15, help_text="聚會標題")
    description = models.TextField(help_text="聚會描述", blank=True)
    address = models.CharField(max_length=255, help_text="聚會地址，例：台北市信義區市府路1號")
    start_time = models.DateTimeField(help_text="聚會開始時間")
    duration = models.PositiveIntegerField(help_text="預估聚會持續時間（小時）", default=1)
    max_participants = models.PositiveIntegerField(help_text="參加人數上限", default=10)
    created_at = models.DateTimeField(auto_now_add=True, help_text="聚會建立時間")
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True, help_text="聚會分類")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_activities', help_text="聚會建立者")
    
    
    @property
    def end_time(self):
        return self.start_time + timedelta(hours=self.duration)

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
    

    @property
    def is_upcoming(self):
        return self.start_time > timezone.now()
    

    @property
    def is_finished(self):
        return self.end_time < timezone.now()


class MeetupPaticipat(models.Model):
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE,related_name='participants', help_text="聚會")
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='meetups', help_text="參與者")
    joined_at = models.DateTimeField(auto_now_add=True, help_text="加入時間")
    
    class Meta:
        unique_together = ('activity', 'participant')
    
    def __str__(self):
        return f"{self.activity.title} - {self.participant.username}（{self.joined_at.strftime('%Y-%m-%d %H:%M')})"