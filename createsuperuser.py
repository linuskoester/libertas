import os
from django.contrib.auth.models import User


if not User.objects.filter(username=os.environ['DJANGO_ADMIN_USERNAME']).exists():
    u = User(username=os.environ['DJANGO_ADMIN_USERNAME'])
    u.set_password(os.environ['DJANGO_ADMIN_PASSWORD'])
    u.is_superuser = True
    u.is_staff = True
    u.save()
    u = User.objects.get(username=os.environ['DJANGO_ADMIN_USERNAME'])
    u.profile.email_confirmed = True
    u.save()
    print('Admin-Account erstellt!')
else:
    print('Admin-Account existiert bereits!')
