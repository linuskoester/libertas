from datetime import datetime, date

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render

from .forms import RedeemForm
from .models import Ausgabe, Code, User

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


def startseite(request):
    ausgaben = Ausgabe.objects.filter(publish_date__lte=date.today())
    inventory = []

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        for ausgabe in ausgaben:
            if Code.objects.filter(user=user, ausgabe=ausgabe).exists():
                inventory.append(ausgabe)

    return render(request, 'libertas/startseite.html', {'menu': 'startseite',
                                                        'ausgaben': ausgaben,
                                                        'inventory': inventory})


def podcast(request):
    return render(request, 'libertas/podcast.html', {'menu': 'podcast'})


def team(request):
    return render(request, 'libertas/team.html', {'menu': 'team'})


def faq(request):
    return render(request, 'libertas/faq.html', {'menu': 'faq'})


def redeem(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'POST':
        form = RedeemForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].upper()
            code = Code.objects.get(code=code)
            code.user = User.objects.get(username=request.user)
            log(request.user, CHANGE, 'Benutzer hat Code %s (%s) eingelöst.' %
                (code.code, code.ausgabe.name))
            code.redeemed = datetime.now()
            code.save()
            messages.success(
                request, 'Du hast jetzt Zugriff auf die Ausgabe <code>%s</code>.' % code.ausgabe.name)
            return redirect('index')
    else:
        form = RedeemForm()

    return render(request, 'libertas/redeem.html', {'menu': 'user-redeem', 'form': form})
