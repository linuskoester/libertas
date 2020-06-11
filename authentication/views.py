import os

from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from libertas.views import log_user, wartung

from .forms import (ChangePasswordForm, DeleteAccountForm, ResetForm,
                    SetPasswordForm, SignInForm, SignUpForm)
from .tokens import reset_token, signup_token


def signin(request):
    # Wartung
    w = wartung(request, "auth")
    if w:
        return w

    # Wenn angemeldet, leite zur Startseite weiter
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            # Melde den Benutzer an
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # Bestätigungsnachricht und leite zur Startseite weiter
            messages.success(
                request, 'Du wurdest erfolgreich angemeldet.')
            return redirect('index')
    else:
        # Wenn Formular noch nicht ausgefüllt, lade Formular in den Kontext
        form = SignInForm()
    return render(request, 'authentication/login.html', {'form': form})


def signout(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    # Melde ab und leite zur Startseite weiter
    logout(request)
    messages.info(request, 'Du wurdest erfolgreich abgemeldet.')
    return redirect('index')


def signup(request):
    # Wartung
    w = wartung(request, "signup")
    if w:
        return w

    # Wenn angemeldet, leite zur Startseite weiter
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Daten aus dem Formular, E-Mail ergänzen
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['username'] + '@halepaghen.de'
            # Wenn Benutzer noch nicht existiert
            if not User.objects.filter(username=username).exists():
                # Erstelle Benutzer + Logeinträge
                user = User.objects.create_user(username, email, password)
                log_user(user, ADDITION, 'Account erstellt.')
                log_user(user, CHANGE,
                         'Registriert und Aktivierungs-Email gesendet.')
                user.save()
            # Wenn Benutzer schon existiert, aber E-Mail nicht bestätigt
            else:
                # Ändere Passwort vom unbestätigten Benutzer + Logeintrag
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                log_user(user, CHANGE,
                         'Registriert und Aktivierungs-Email gesendet.')
                # Die Form Validierung fängt alle Accounts ab, die bereits existieren
                # und eine bestätigte E-Mail-Adresse haben. D.h. wird dieser Skript
                # nicht ausgeführt, wenn der Account eine bestätigte E-Mail-Adresse hat.
            # Sende Bestätigungs-Email
            subject = 'Aktiviere deinen TheHaps-Account'
            message = render_to_string('authentication/signup_email.html', {
                'user': user,
                'domain': os.environ['LIBERTAS_DOMAIN'],
                'beta': bool(int(os.environ['LIBERTAS_BETA'])),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': signup_token.make_token(user),
            })
            user.email_user(subject, message)
            # Zeige Bestätigungsnachricht
            messages.success(request,
                             """Wir haben dir eine E-Mail mit einem Bestätigungslink gesendet.
                                Gehe jetzt auf IServ und klicke auf den Link, um deinen Account
                                zu aktivieren!<br>
                                <a class="btn btn-outline-success mt-2" href="https://halepaghen.de/">
                                Weiter zu IServ</a>""")
            return redirect('index')
    else:
        # Wenn Formular noch nicht ausgefüllt, lade Formular in den Kontext
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


def signup_activate(request, uidb64, token):
    # Wartung
    w = wartung(request, "signup")
    if w:
        return w

    # Versuche aus der URL den Benutzer auszulesen
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        # Falls Benutzer nicht existiert
        user = None

    # Überprüfe ob URL/Token gültig
    if user is not None and signup_token.check_token(user, token):
        # Setze E-Mail auf bestätigt + Logeintrag
        user.profile.email_confirmed = True
        user.save()
        log_user(user, CHANGE, 'Account bestätigt.')
        # Melde Benutzer an
        login(request, user)
        # Bestätigungsnachricht und Weiterleitung zur Startseite
        messages.success(
            request, 'Du hast deine E-Mail-Adresse bestätigt, dein Account wurde erfolgreich aktiviert.')
        return redirect('index')
    # Wenn URL ungültig
    else:
        # Falls Benutzer angemeldet, lade zur Startseite weiter und ignoriere den falschen Link
        if request.user.is_authenticated:
            return redirect('index')
        # Wenn nicht angemeldet, zeige Fehlermeldung
        else:
            # Zeige Fehlermeldung
            messages.error(request,
                           'Dieser Bestätigungslink ist ungültig oder wurde bereits verwendet.')
            return redirect('index')


def reset(request):
    # Wartung
    w = wartung(request, "auth")
    if w:
        return w

    # Wenn angemeldet, leite zur Startseite weiter
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            # Benutzername aus Formular
            username = form.cleaned_data['username']
            # Wenn Benutzer existiert
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                # Sende Passwort-Zurücksetz-Mail
                subject = 'Setzte das Passwort von deinem TheHaps-Account zurück'
                message = render_to_string('authentication/reset_email.html', {
                    'user': user,
                    'domain': os.environ['LIBERTAS_DOMAIN'],
                    'beta': bool(int(os.environ['LIBERTAS_BETA'])),
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': reset_token.make_token(user),
                })
                user.email_user(subject, message)
                # Logeintrag
                log_user(
                    user, CHANGE, 'Zurücksetzen des Passworts angefordert, Link gesendet.')
            # Zeige Bestätigungsnachricht
            messages.success(request,
                             """Sofern ein Account mit dieser E-Mail-Adresse existiert,
                                haben wir dir eine E-Mail mit einem Bestätigungslink gesendet.<br>
                                Gehe jetzt auf IServ und klicke auf den Link, um dein
                                Passwort zurückzusetzen.<br>
                                <a class="btn btn-outline-success mt-2" href="https://halepaghen.de/">
                                Weiter zu IServ</a>""")
            return redirect('index')
    else:
        # Wenn Formular noch nicht ausgefüllt, lade Formular in den Kontext
        form = ResetForm()
    return render(request, 'authentication/reset.html', {'form': form})


def reset_confirm(request, uidb64, token):
    # Wartung
    w = wartung(request, "auth")
    if w:
        return w

    # Versuche aus der URL den Benutzer auszulesen
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        # Wenn Benutzer nicht existiert
        user = None

    # Wenn URL, Benutzer und Token gültig
    if user is not None and reset_token.check_token(user, token):
        # Wenn Formular ausgefüllt
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                # Ändere Passwort
                user.set_password(form.cleaned_data['password'])
                log_user(user, CHANGE, 'Passwort zurückgesetzt.')
                # Falls E-Mail noch nicht bestätigt, ändere sie zu bestätigt + Logeintrag
                if not user.profile.email_confirmed:
                    user.profile.email_confirmed = True
                    log_user(user, CHANGE,
                             'E-Mail durch Zurücksetzen des Passworts bestätigt.')
                # Speichere Benutzer
                user.save()
                # Leite zum Login weiter
                messages.success(request,
                                 """Dein Passwort wurde erfolgreich zurückgesetzt. Du kannst dich jetzt mit
                                 deinem neuen Passwort anmelden!""")
                return redirect('signin')
        else:
            # Wenn Formular noch nicht ausgefüllt, lade Formular in den Kontext
            form = SetPasswordForm()
        return render(request, 'authentication/reset_set_password.html', {'form': form})
    else:
        # Wenn Link falschund  Benutzer angemeldet, lade zur Startseite weiter und ignoriere den falschen Link
        if request.user.is_authenticated:
            return redirect('index')
        # Wenn Link falsch und nicht angemeldet, zeige Fehlermeldung
        else:
            # Zeige Fehlermeldung
            messages.error(request,
                           'Dieser Bestätigungslink ist ungültig oder wurde bereits verwendet.')
            return redirect('index')


def account_info(request):
    # Wartung
    w = wartung(request, "auth")
    if w:
        return w

    # Falls Benutzer angemeldet
    if request.user.is_authenticated:
        return render(request, 'authentication/account_account.html', {'menu': 'user-account-account'})
    else:
        # Leite zur Anmeldeseite weiter
        return redirect('signin')


def account_password(request):
    # Wartung
    w = wartung(request, "auth")
    if w:
        return w

    # Falls Benutzer angemeldet
    if request.user.is_authenticated:
        # Wenn Passwort-Zurücksetz-Formular ausgefüllt
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                # Authentifiziere Benutzer
                user = authenticate(
                    request, username=request.user.username, password=form.cleaned_data['password_old'])
                # Wenn Authentifizierung erfolgreich
                if user is not None:
                    # Ändere Passwort + Logeintrag
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    log_user(user, CHANGE, 'Passwort vom Benutzer geändert.')
                    # Bestätigungsnachricht
                    messages.success(
                        request, 'Dein Passwort wurde erfolgreich geändert.')
                    # Melde Benutzer mit neuem Passwort an
                    login(request, user)
                # Wenn Authentifizierung fehlgeschlagen
                else:
                    # Zeige Fehlermeldung
                    form.add_error('password_old', 'Das Passwort ist falsch.')
        else:
            # Wenn Formular noch nicht ausgefüllt, lade Formular in den Kontext
            form = ChangePasswordForm()
        return render(request, 'authentication/account_password.html', {'menu': 'user-account-password', 'form': form})
    # Wenn Benutzer nicht angemeldet
    else:
        # Leite zur Anmeldeseite weiter
        return redirect('signin')


def account_delete(request):
    # Wartung
    w = wartung(request, "auth")
    if w:
        return w

    # Wenn Benutzer angemeldet
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DeleteAccountForm(request.POST)
            if form.is_valid():
                # Authentifiziere Benutzer
                user = authenticate(
                    username=request.user.username, password=form.cleaned_data['password'])
                # Wenn Authentifizierung erfolgreich
                if user is not None:
                    # Lösche Benutzer
                    user.delete()
                    # Zeige Bestätigungsnachricht und leite zur Startseite weiter
                    messages.warning(
                        request, 'Dein Account wurde erfolgreich gelöscht.')
                    return redirect('index')
                # Wenn Authentifizierung fehlgeschlagen
                else:
                    # Zeige Fehlermeldung
                    form.add_error('password', 'Das Passwort ist falsch.')
                    # Lässt sich nicht in als Validation in forms.py schreiben,
                    # da die clean()-Funktion kein Zugriff auf request hat, und
                    # somit den Benutzernamen nicht kennt.
        else:
            # Wenn Formular noch nicht ausgefüllt, lade Formular in den Kontext
            form = DeleteAccountForm()
        return render(request, 'authentication/account_delete.html', {'menu': 'user-account-delete', 'form': form})
    # Wenn nicht angemeldet
    else:
        # Leite zur Anmelde-Seite weiter
        return redirect('signin')
