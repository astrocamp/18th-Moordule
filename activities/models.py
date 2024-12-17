from django.conf import settings
from django.db import models
from django.utils import timezone


class Activity(models.Model):
    # """
    # Activity
    # 欄位說明：
    # - title: 活動名稱或主題。
    # - description: 活動描述。
    # - location_area: 活動所在區域(如台北市信義區)
    # - start_time, end_time: 活動開始與結束時間。
    # - max_participants: 活動限制的人數上限。
    # - creator: 活動創建者(透過外部User或Member模型)。
    # - created_at: 活動建立時間。

    # 後續擴充可以新增：
    # - tags、image、budget_type、event_type等欄位。
    # - 參加者中介模型(Participation)、留言模型(Comment)、回饋模型(Feedback)。
    # - 金流相關(Wallet等)。
    # """

    title = models.CharField(max_length=100, help_text="活動標題")
    description = models.TextField(help_text="活動描述", blank=True)
    address = models.CharField(
        max_length=255, help_text="活動地址，例：台北市信義區市府路1號"
    )
    start_time = models.DateTimeField(help_text="活動開始時間")
    end_time = models.DateTimeField(
        null=True, blank=True, help_text="活動結束時間(選填)"
    )
    max_participants = models.PositiveIntegerField(help_text="參加人數上限", default=10)

    # 此處的creator為簡化，未來整合會員系統時，把 AUTH_USER_MODEL 改成實際的會員模型
    # 目前先使用 settings.AUTH_USER_MODEL
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_activities",
        help_text="活動創辦人",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="活動建立時間")

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

    @property
    def is_upcoming(self):
        return self.start_time > timezone.now()

    @property
    def is_finished(self):
        if self.end_time:
            return self.end_time < timezone.now()
        return False
