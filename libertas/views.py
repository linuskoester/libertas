from datetime import datetime, date

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render

from .forms import RedeemForm
from .models import Ausgabe, Code, User, Configuration
from django.contrib.auth import logout

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


def wartung(request):
    if Configuration.objects.get(name="Einstellungen").wartung_voll:
        if request.user.is_superuser:
            messages.error(request, 'Wartungsmodus (Voll) aktiviert!')
        else:
            return True

    if Configuration.objects.get(name="Einstellungen").wartung_auth:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                messages.error(
                    request, 'Wartungsmodus (Authentifizierungssystem) aktiviert!')
            else:
                messages.warning(
                    request, 'Du wurdest aufgrund von Wartungsarbeiten abgemeldet.')
                logout(request)

    if Configuration.objects.get(name="Einstellungen").wartung_signup:
        if request.user.is_superuser:
            messages.error(request, 'Wartungsmodus (Registrierung) aktiviert!')

    if Configuration.objects.get(name="Einstellungen").wartung_viewer:
        if request.user.is_superuser:
            messages.error(request, 'Wartungsmodus (Viewer) aktiviert!')


def startseite(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    ausgaben = Ausgabe.objects.filter(publish_date__lte=date.today())
    inventory = []

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        for ausgabe in ausgaben:
            if Code.objects.filter(user=user, ausgabe=ausgabe).exists():
                inventory.append(ausgabe)

    return render(request, 'libertas/startseite.html', {'menu': 'sz-start',
                                                        'ausgaben': ausgaben,
                                                        'inventory': inventory})


def podcast(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    return render(request, 'libertas/podcast.html', {'menu': 'podcast'})


def team(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    return render(request, 'libertas/team.html', {'menu': 'sz-team'})


def faq(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    return render(request, 'libertas/faq.html', {'menu': 'sz-faq'})


def redeem(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

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
