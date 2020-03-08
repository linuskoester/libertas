from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from .models import Ausgabe, Token, User
from .forms import RedeemForm
from datetime import datetime
from django.contrib import messages
# from django.contrib import messages


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
    ausgaben = Ausgabe.objects

    return render(request, 'libertas/index.html', {'ausgaben': ausgaben})


def redeem(request, number):
    if not request.user.is_authenticated:
        return redirect('index')
    ausgabe = get_object_or_404(Ausgabe, number=number)
    if request.method == 'POST':
        form = RedeemForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token'].upper()
            token = Token.objects.get(token=token)
            if token.ausgabe is None:
                token.ausgabe = ausgabe
            token.user = User.objects.get(username=request.user)
            token.redeemed = datetime.now()
            token.save()
            messages.success(request, 'Du hast jetzt Zugriff auf die Ausgabe "%s".' % token.ausgabe.name)
            return redirect('index')
    else:
        form = RedeemForm()

    return render(request, 'libertas/redeem.html', {'form': form})
