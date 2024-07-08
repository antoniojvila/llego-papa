from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a default superuser'

    def handle(self, *args, **kwargs):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user = User.objects.get(username=username)
            user.role = 'profesor'
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}"'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists'))
