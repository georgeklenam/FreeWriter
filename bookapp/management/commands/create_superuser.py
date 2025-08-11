from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@freewriter.com'
        password = 'f001'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser "{username}" already exists.')
            return
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Password: {password}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to create superuser: {e}')
            )
