from django.db import models
from django.utils import timezone
from datetime import timedelta

   
class Category(models.Model):
    name = models.CharField(max_length=15, help_text="分類名稱")
    description = models.TextField(help_text="分類描述", blank=True, null=True)
    order = models.PositiveIntegerField(help_text="排序", default=0)

    def __str__(self):
        return self.name


# 活動模型  
class Activity(models.Model):
    title = models.CharField(max_length=15, help_text="活動標題")
    description = models.TextField(help_text="活動描述", blank=True)
    address = models.CharField(max_length=255, help_text="活動地址，例：台北市信義區市府路1號")
    start_time = models.DateTimeField(help_text="活動開始時間")
    duration = models.PositiveIntegerField(help_text="預估活動持續時間（小時）", default=1)
    max_participants = models.PositiveIntegerField(help_text="參加人數上限", default=10)
    created_at = models.DateTimeField(auto_now_add=True, help_text="活動建立時間")
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True, help_text="活動分類")
    # 活動結束時間是動態推算出來的
    @property
    def end_time(self):
        return self.start_time + timedelta(hours=self.duration)

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
    
    # 判斷活動是否即將開始
    @property
    def is_upcoming(self):
        return self.start_time > timezone.now()
    
    # 判斷活動是否已經結束
    @property
    def is_finished(self):
        return self.end_time < timezone.now()
