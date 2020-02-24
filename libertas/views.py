from django.shortcuts import render
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


def log(user, flag, message):
    # Funktion um Einträge bei Objektem im Django-Admin zu loggen
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(
            user).pk,
        object_id=user.id,
        object_repr=user.username,
        action_flag=flag,
        change_message=message)


def index(request):
    # Startseite
    return render(request, 'libertas/index.html')
