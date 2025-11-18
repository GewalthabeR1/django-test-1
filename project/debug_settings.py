import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.conf import settings

print("=== DATABASES CONFIG ===")
print(settings.DATABASES['default']['ENGINE'])
print(settings.DATABASES['default']['NAME'])