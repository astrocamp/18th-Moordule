import random
from datetime import timedelta
from decimal import Decimal
from io import BytesIO

import requests
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from PIL import Image

from activities.models import Activity, MeetupPaticipat
from users.models import Record


class Command(BaseCommand):
    help = "生成假資料"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=10, help="要生成的使用者數量")
        parser.add_argument(
            "--activities", type=int, default=30, help="要生成的活動數量"
        )
        parser.add_argument(
            "--topups", type=int, default=50, help="要生成的儲值記錄數量"
        )
        parser.add_argument("--no-images", action="store_true", help="不生成圖片")

    def get_random_image(self, width, height, is_avatar=False):
        """使用 picsum.photos 獲取隨機圖片"""
        try:
            url = (
                f"https://picsum.photos/{width}/{height}"
                if not is_avatar
                else f"https://picsum.photos/200"
            )
            response = requests.get(url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img_io = BytesIO()
                if img.format == "PNG":
                    img = img.convert("RGB")
                img.save(img_io, format="JPEG", quality=85)
                img_io.seek(0)
                return img_io
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"下載圖片時發生錯誤: {e}"))
        return None

    def create_users(self, num_users, fake, no_images):
        """創建假使用者資料"""
        self.stdout.write("創建使用者...")
        CustomUser = get_user_model()
        users = []

        for i in range(num_users):
            gender = random.choice([choice[0] for choice in CustomUser.GENDER_CHOICES])
            hobbies = random.sample(
                [choice[0] for choice in CustomUser.HOBBY_CHOICES], random.randint(1, 4)
            )

            user = CustomUser(
                username=fake.user_name(),
                email=fake.email(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=70),
                gender=gender,
                bio=fake.text(max_nb_chars=200),
                live_in=random.choice(
                    [choice[0] for choice in CustomUser.CITIES_CHOICES]
                ),
                hobbies=hobbies,
            )
            user.set_password("password123")  # 設定預設密碼
            user.save()

            if not no_images:
                avatar_io = self.get_random_image(200, 200, is_avatar=True)
                if avatar_io:
                    user.avatar.save(
                        f"avatar_{user.username}.jpg", File(avatar_io), save=True
                    )

            users.append(user)
            self.stdout.write(self.style.SUCCESS(f"創建使用者 {i+1}/{num_users}"))

        return users

    def create_activities(self, users, num_activities, fake, no_images):
        """創建假活動資料"""
        self.stdout.write("創建活動...")
        activities = []

        for i in range(num_activities):
            owner = random.choice(users)
            hobby = random.choice(owner.hobbies)

            # 隨機生成活動時間，偏向未來時間
            days_offset = random.randint(-5, 30)  # 調整範圍，使更多活動在未來
            start_time = timezone.now() + timedelta(
                days=days_offset, hours=random.randint(0, 23)
            )

            activity = Activity(
                title=f"{fake.word()} {hobby}"[:15],
                description=fake.text(max_nb_chars=500),
                address=fake.address(),
                start_time=start_time,
                duration=random.randint(1, 4),
                max_participants=random.randint(3, 20),
                owner=owner,
            )

            if not no_images:
                image_io = self.get_random_image(1280, 720)
                if image_io:
                    activity.photo.save(
                        f"activity_{activity.title}.jpg", File(image_io), save=True
                    )

            activity.save()

            # 為活動添加參與者
            num_participants = random.randint(
                1, min(activity.max_participants, len(users) - 1)
            )
            potential_participants = [u for u in users if u != owner]
            if potential_participants:  # 確保有可用的參與者
                participants = random.sample(potential_participants, num_participants)

                for participant in participants:
                    join_days = (
                        min(days_offset + 30, 0)
                        if days_offset < 0
                        else random.randint(0, days_offset)
                    )
                    MeetupPaticipat.objects.create(
                        activity=activity,
                        participant=participant,
                        joined_at=timezone.now() - timedelta(days=join_days),
                    )

            activities.append(activity)
            self.stdout.write(self.style.SUCCESS(f"創建活動 {i+1}/{num_activities}"))

        return activities

    def create_records(self, users, activities, num_topups, fake):
        """創建記錄資料"""
        self.stdout.write("創建記錄...")
        payment_methods = ["信用卡", "Line Pay", "街口支付", "超商代碼"]

        # 活動記錄
        record_count = 0
        for activity in activities:
            participants = activity.participants.all()

            for participant in participants:
                Record.objects.create(
                    amount=Decimal(str(random.randint(100, 1000))),
                    user=participant.participant,
                    type="meetup",
                    notes={"topic": activity.title},
                )
                record_count += 1
                if record_count % 10 == 0:  # 調整顯示頻率
                    self.stdout.write(f"已創建 {record_count} 筆記錄")

        # 儲值記錄
        for i in range(num_topups):
            user = random.choice(users)
            Record.objects.create(
                amount=Decimal(str(random.randint(500, 5000))),
                user=user,
                type="topup",
                notes={"payment_method": random.choice(payment_methods)},
            )
            if (i + 1) % 10 == 0:  # 調整顯示頻率
                self.stdout.write(f"已創建 {i+1}/{num_topups} 筆儲值記錄")

    def handle(self, *args, **options):
        fake = Faker(["zh_TW"])
        num_users = options["users"]
        num_activities = options["activities"]
        num_topups = options["topups"]
        no_images = options["no_images"]

        self.stdout.write("開始清理舊資料...")
        Record.objects.all().delete()
        MeetupPaticipat.objects.all().delete()
        Activity.objects.all().delete()
        get_user_model().objects.filter(is_superuser=False).delete()

        self.stdout.write("開始生成假資料...")
        users = self.create_users(num_users, fake, no_images)
        activities = self.create_activities(users, num_activities, fake, no_images)
        self.create_records(users, activities, num_topups, fake)

        self.stdout.write(self.style.SUCCESS("假資料生成完成！"))
