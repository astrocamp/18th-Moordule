from django.core.management.base import BaseCommand
from activities.models import MyModel

class Command(BaseCommand):
    help = 'Populate initial data'

    def handle(self, *args, **kwargs):
        MyModel.objects.create(name='Example', value=123)
        self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))