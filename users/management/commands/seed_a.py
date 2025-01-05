# management/commands/seed_data.py
import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from activities.models import Activity, Category, MeetupPaticipat
from users.models import CustomUser, Record

fake = Faker("zh_TW")


class Command(BaseCommand):
    help = "生成測試數據"

    def handle(self, *args, **kwargs):
        self.stdout.write("開始生成測試數據...")

        # 創建用戶
        users = []
        for _ in range(20):
            gender = random.choice(["male", "female", "other"])

            user = CustomUser.objects.create(
                email=fake.email(),
                username=fake.name(),
                bio=fake.text(max_nb_chars=200),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=70),
                gender=gender,
                live_in=random.choice([x[0] for x in CustomUser.CITIES_CHOICES]),
                hobbies=random.sample(
                    [x[0] for x in CustomUser.HOBBY_CHOICES], k=random.randint(1, 4)
                ),
            )
            user.set_password("password123")
            user.save()
            users.append(user)

        categories = []
        for hobby_code, hobby_name in CustomUser.HOBBY_CHOICES:
            category = Category.objects.create(
                name=hobby_name,
                description=f"{hobby_name}相關活動",
                order=len(categories),
            )
            categories.append(category)

        activities = []
        for _ in range(30):
            start_time = timezone.now() + timedelta(days=random.randint(-5, 30))
            category = random.choice(categories)
            activity = Activity.objects.create(
                title=f"{category.name}聚會",
                description=f"一起來{category.name}吧！{fake.text(max_nb_chars=150)}",
                address=fake.address(),
                start_time=start_time,
                duration=random.randint(1, 5),
                max_participants=random.randint(5, 20),
                category=category,
                owner=random.choice(users),
            )
            activities.append(activity)

        for activity in activities:
            participant_count = random.randint(
                1, min(len(users), activity.max_participants)
            )
            participants = random.sample(
                [u for u in users if u != activity.owner], k=participant_count
            )

            for user in participants:
                MeetupPaticipat.objects.create(activity=activity, participant=user)

        for user in users:
            for _ in range(random.randint(3, 8)):
                record_type = random.choice(["meetup", "topup"])
                amount = Decimal(str(random.randint(100, 1000)))

                record = Record.objects.create(
                    amount=amount, user=user, type=record_type
                )

                if record_type == "meetup":
                    record.set_notes(topic=f"{random.choice(categories).name}相關活動")
                else:
                    record.set_notes(
                        payment_method=random.choice(["街口支付", "LINE Pay", "信用卡"])
                    )
                record.save()

        self.stdout.write(self.style.SUCCESS("成功生成測試數據！"))
