from django.shortcuts import redirect, render
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from .models import Ausgabe, Code, User
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

    inventory = []
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        for ausgabe in Ausgabe.objects.all():
            if Code.objects.filter(user=user, ausgabe=ausgabe).exists():
                inventory.append(ausgabe)

    return render(request, 'libertas/index.html', {'menu': 'ausgaben', 'ausgaben': ausgaben, 'inventory': inventory})


def redeem(request):
    if request.method == 'POST':
        form = RedeemForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].upper()
            code = Code.objects.get(code=code)
            code.user = User.objects.get(username=request.user)
            code.redeemed = datetime.now()
            code.save()
            messages.success(
                request, 'Du hast jetzt Zugriff auf die Ausgabe <code>%s</code>.' % code.ausgabe.name)
            return redirect('index')
    else:
        form = RedeemForm()

    return render(request, 'libertas/redeem.html', {'menu': 'user-redeem', 'form': form})
