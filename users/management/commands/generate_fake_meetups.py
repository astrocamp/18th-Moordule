import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from activities.models import Activity, Category, MeetupPaticipat

User = get_user_model()


class Command(BaseCommand):
    help = "產生活動相關假資料"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=20, help="每個分類要產生的活動數量"
        )

    def handle(self, *args, **options):
        fake = Faker(["zh_TW"])
        activity_count = options["count"]

        # 先檢查是否有使用者
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR("請先創建使用者"))
            return

        # 創建分類
        activity_types = ["吃飯", "喝酒", "唱歌", "運動", "電影", "討論"]
        categories = []

        for i, type_name in enumerate(activity_types):
            category, created = Category.objects.get_or_create(
                name=type_name,
                defaults={"description": fake.text(max_nb_chars=100), "order": i},
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {type_name}"))

        # 創建活動
        locations = [
            "台北市信義區市府路1號",
            "台北市大安區忠孝東路四段",
            "新北市板橋區文化路一段",
            "台北市中山區林森北路",
            "台北市大安區師大路",
        ]

        # 為每個分類創建活動
        for category in categories:
            for _ in range(activity_count):
                # 隨機選擇開始時間（未來 30 天內）
                start_time = timezone.now() + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )

                try:
                    activity = Activity.objects.create(
                        title=f"{category.name}-{fake.word()}",
                        description=fake.text(max_nb_chars=200),
                        address=random.choice(locations),
                        start_time=start_time,
                        duration=random.randint(1, 4),
                        max_participants=random.randint(2, 15),
                        category=category,
                        owner=random.choice(users),
                    )

                    participant_count = random.randint(1, activity.max_participants)
                    random_users = random.sample(list(users), participant_count)

                    for user in random_users:
                        try:
                            MeetupPaticipat.objects.create(
                                activity=activity, participant=user
                            )
                        except Exception as e:
                            continue

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created activity: {activity.title} with {participant_count} participants"
                        )
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to create activity: {str(e)}")
                    )
