# generate_fake_data.py
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = "產生假用戶資料"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, help="要創建的用戶數量")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        fake = Faker(["zh_TW"])

        hobby_choices = [choice[0] for choice in User.HOBBY_CHOICES]
        gender_choices = [choice[0] for choice in User.GENDER_CHOICES]

        cities = [
            "台北市",
            "新北市",
            "桃園市",
            "台中市",
            "台南市",
            "高雄市",
            "基隆市",
            "新竹市",
            "嘉義市",
        ]

        for i in range(count):
            email = fake.email()

            try:
                user = User.objects.create(
                    username=fake.user_name(),
                    email=email,
                    birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    gender=random.choice(gender_choices),
                    live_in=random.choice(cities),
                    hobbies=random.sample(hobby_choices, random.randint(1, 3)),
                )

                user.set_password("password123")
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created user: {email}")
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to create user: {email}, error: {str(e)}")
                )
