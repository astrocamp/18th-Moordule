import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from activities.models import Activity as Meetups

User = get_user_model()


class Command(BaseCommand):
    help = "生成假聚會資料"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=20, help="要生成的聚會數量(預設: 20)")
        parser.add_argument("--force", action="store_true", help="強制重新生成（會刪除現有聚會）")

    def format_datetime(self, dt):
        """格式化日期時間，並處理 None 的情況"""
        if dt is None:
            return "未設定時間"
        return dt.strftime("%Y-%m-%d %H:%M")

    def format_time(self, dt):
        """格式化時間，並處理 None 的情況"""
        if dt is None:
            return "未設定時間"
        return dt.strftime("%H:%M")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        force = kwargs.get("force", False)
        fake = Faker("zh_TW")

        # 檢查是否有用戶
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR("找不到用戶，請先建立用戶"))
            return

        # 如果是強制模式，先刪除現有聚會
        if force:
            deleted_count = Meetups.objects.all().delete()[0]
            self.stdout.write(f"已刪除 {deleted_count} 個現有聚會")

        # 定義常用值
        activity_types = [
            "聚餐",
            "電影",
            "運動",
            "讀書會",
            "桌遊",
            "爬山",
            "烤肉",
            "唱歌",
        ]
        areas = ["信義區", "大安區", "中山區", "內湖區", "松山區", "南港區"]

        # 批次創建聚會
        meetups = []
        try:
            for i in range(count):
                activity_type = random.choice(activity_types)
                area = random.choice(areas)

                start_time = timezone.now() + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )
                end_time = start_time + timedelta(hours=random.randint(1, 4))

                meetup = Meetups(
                    title=f"{activity_type}：{fake.catch_phrase()}",
                    description=fake.text(max_nb_chars=200),
                    address=f"台北市{area}{fake.street_address()}",
                    start_time=start_time,
                    end_time=end_time,
                    max_participants=random.randint(2, 20),
                    creator=random.choice(users),
                )
                meetups.append(meetup)
                self.stdout.write(f"準備第 {i+1} 個聚會")

            # 批次創建
            created_meetups = Meetups.objects.bulk_create(meetups)

            self.stdout.write(self.style.SUCCESS(f"成功創建 {len(created_meetups)} 個聚會"))

            # 列出創建的聚會資訊
            self.stdout.write("\n創建的聚會列表:")
            for meetup in created_meetups:
                start_time_str = self.format_datetime(meetup.start_time)
                end_time_str = self.format_time(meetup.end_time)

                self.stdout.write(
                    f"聚會: {meetup.title}\n"
                    f"時間: {start_time_str} - {end_time_str}\n"
                    f"地點: {meetup.address}\n"
                    f"建立者: {meetup.creator.username}\n"
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"創建聚會時發生錯誤: {str(e)}"))
