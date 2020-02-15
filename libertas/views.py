from django.shortcuts import render
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

# Create your views here.


def log(user, flag, message):
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(
            user).pk,
        object_id=user.id,
        object_repr=user.username,
        action_flag=flag,
        change_message=message)


def index(request):
    message = request.GET.get('message')
    if message == 'signout':
        messages.info(request, 'Du wurdest erfolgreich abgemeldet.')
    elif message == 'signin':
        messages.success(request, 'Du wurdest erfolgreich angemeldet.')
    elif message == 'deleted':
        messages.info(request, 'Dein Account wurde erfolgreich gelöscht.')
    elif message == 'activated':
        messages.success(
            request, 'Du hast deine E-Mail-Adresse bestätigt, dein Account wurde erfolgreich aktiviert.')
    return render(request, 'libertas/index.html')
