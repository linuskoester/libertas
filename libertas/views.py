from datetime import datetime, date

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render

from .forms import RedeemForm, CoronaForm
from .models import Ausgabe, Code, User, Configuration
from django.contrib.auth import logout
from django.template.loader import render_to_string
import os

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

    if Configuration.objects.get(name="Einstellungen").wartung_corona:
        if request.user.is_superuser:
            messages.error(
                request, 'Wartungsmodus (Corona-Bestellsystem) aktiviert!')


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


def datenschutz(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    return render(request, 'libertas/datenschutz.html')


def agb(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    return render(request, 'libertas/agb.html')


def impressum(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    return render(request, 'libertas/impressum.html')


def corona(request):
    if wartung(request):
        return render(request, 'libertas/wartung.html')

    if Configuration.objects.get(name="Einstellungen").wartung_corona:
        wartungsmodus = True
    else:
        wartungsmodus = False

    published = False
    besitz = False
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if Ausgabe.objects.filter(number=1).exists():
            ausgabe = Ausgabe.objects.get(number=1)
            if date.today() >= ausgabe.publish_date:
                published = True

            if Code.objects.filter(user=user, ausgabe=ausgabe).exists():
                besitz = True

    if request.method == 'POST':
        form = CoronaForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            user.profile.corona_bestellung = True
            user.save()

            code = Code(ausgabe=Ausgabe.objects.get(number=1))
            code.save()

            code = Code.objects.get(code=code.code)
            print(code)

            log(request.user, CHANGE, 'Der Benutzer hat durch das Corona-Bestellsystem den Code %s (%s) bestellt.' %
                (code.code, code.ausgabe.name))
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(
                    code).pk,
                object_id=code.code,
                object_repr=request.user.username,
                action_flag=CHANGE,
                change_message='Wurde von Benutzer über das Corona-Bestellsystem bestellt.')

            subject = 'Dein Zugangscode für die digitale Ausgabe von TheHaps ist da!'
            message = render_to_string('libertas/corona_email.html', {
                'user': user,
                'domain': os.environ['LIBERTAS_DOMAIN'],
                'code': code.code
            })
            user.email_user(subject, message)

            messages.success(
                request, 'Dein Zugangscode wurde erfolgreich an <code>%s</code> gemailt.' % request.user.email)

            return redirect('index')
    else:
        form = CoronaForm()

    return render(request, 'libertas/corona.html', {'form': form,
                                                    'published': published,
                                                    'besitz': besitz,
                                                    'wartung': wartungsmodus},)
