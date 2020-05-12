from datetime import datetime, date
from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
from .forms import RedeemForm, CoronaForm
from .models import Ausgabe, Code, User, Configuration, ausgaben_visible, ausgaben_user
from django.contrib.auth import logout
from django.template.loader import render_to_string
import os


def log_user(user, flag, message):
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(
            user).pk,
        object_id=user.id,
        object_repr=user.username,
        action_flag=flag,
        change_message=message)


def wartung(request, pagetype=""):
    wartung = Configuration.objects.get(name="Einstellungen")
    if request.user.is_superuser:
        if wartung.voll():
            messages.warning(request, 'Wartungsmodus (Voll) aktiviert!')
        if wartung.auth():
            messages.warning(request, 'Wartungsmodus (Auth.) aktiviert!')
        if wartung.signup():
            messages.warning(request, 'Wartungsmodus (Regist.) aktiviert!')
        if wartung.viewer():
            messages.warning(request, 'Wartungsmodus (Viewer) aktiviert!')
        if wartung.corona():
            messages.warning(request, 'Wartungsmodus (Corona) aktiviert!')
    else:
        if wartung.voll():
            return render(request, 'libertas/wartung.html')
        if wartung.auth():
            if request.user.is_authenticated:
                messages.warning(
                    request, 'Du wurdest aufgrund von Wartungsarbeiten abgemeldet.')
                logout(request)
            elif pagetype == "auth" or pagetype == "signup":
                messages.error(
                    request, """Zurzeit ist die Anmeldung und Registrierung aufgrund von Wartungsarbeiten nicht möglich.
                                <a href="https://status.thehaps.de/">Hier</a> findest du mehr Informationen.""")
                return redirect('index')
        if wartung.signup() and pagetype == "signup":
            messages.error(
                request, """Zurzeit ist die Registrierung aufgrund von Wartungsarbeiten nicht möglich.
                            <a href="https://status.thehaps.de/">Hier</a> findest du mehr Informationen.""")
            return redirect('index')
        if wartung.viewer() and pagetype == "viewer":
            messages.error(
                request, """Aufgrund von Wartungsarbeiten lassen sich zurzeit keine digitalen Ausgaben und Leseproben lesen.
                            <a href="https://status.thehaps.de/">Hier</a> findest du mehr Informationen.""")
            return redirect('index')
        if wartung.corona() and pagetype == "corona":
            return True
    return False


def startseite(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    ausgaben = ausgaben_visible()
    inventory = ausgaben_user(request.user)

    return render(request, 'libertas/startseite.html', {'menu': 'sz-start',
                                                        'ausgaben': ausgaben,
                                                        'inventory': inventory})


def podcast(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/podcast.html', {'menu': 'podcast'})


def team(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/team.html', {'menu': 'sz-team'})


def faq(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/faq.html', {'menu': 'sz-faq'})


def redeem(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'POST':
        form = RedeemForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].upper()
            code = Code.objects.get(code=code)
            code.user = User.objects.get(username=request.user)
            log_user(request.user, CHANGE, 'Benutzer hat Code %s (%s) eingelöst.' %
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
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/datenschutz.html')


def agb(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/agb.html')


def impressum(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/impressum.html')


def corona(request):
    # Wartung
    w = wartung(request, "corona")
    if w is True:
        wartungsmodus = True
    elif w:
        return w
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

            log_user(request.user, CHANGE,
                     'Der Benutzer hat durch das Corona-Bestellsystem den Code %s (%s) bestellt.' %
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
