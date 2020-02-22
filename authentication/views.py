from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm, SignInForm, ResetForm, SetPasswordForm, ChangePasswordForm, DeleteAccountForm
from .tokens import signup_token, reset_token
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
import os

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


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_active:
                    form.add_error(
                        None,
                        'Dein Account wurde manuell deaktiviert.'
                    )
                elif not user.profile.email_confirmed:
                    form.add_error(
                        'username',
                        """Du musst deine E-Mail-Adresse zuerst bestätigen, um dich anzumelden.
                           Solltest du keine Bestätigungs-Mail erhalten haben, klicke unten auf
                           "Passwort vergessen" und setze dein Passwort zurück. Dadurch wird
                           dein Account aktiviert."""
                    )
                else:
                    login(request, user)
                    messages.success(
                        request, 'Du wurdest erfolgreich angemeldet.')
                    return redirect('index')
            else:
                form.add_error(
                    None,
                    'Der Account existiert nicht oder das Passwort ist falsch!'
                )
    else:
        form = SignInForm()
    return render(request, 'authentication/login.html', {'form': form})


def signout(request):
    logout(request)
    messages.info(request, 'Du wurdest erfolgreich abgemeldet.')
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['username'] + '@halepaghen.de'
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                log(user, CHANGE, 'Registriert und Aktivierungs-Email gesendet.')
            else:
                user = User.objects.create_user(username, email, password)
                log(user, ADDITION, 'Account erstellt.')
                log(user, CHANGE, 'Registriert und Aktivierungs-Email gesendet.')
                user.save()

            subject = 'Aktiviere deinen TheHaps-Account'
            message = render_to_string('authentication/signup_email.html', {
                'user': user,
                'domain': os.environ['LIBERTAS_DOMAIN'],
                'beta': bool(int(os.environ['LIBERTAS_BETA'])),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': signup_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('signup_sent')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


def signup_sent(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'authentication/signup_sent.html')


def signup_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and signup_token.check_token(user, token):
        user.profile.email_confirmed = True
        user.save()
        log(user, CHANGE, 'Account bestätigt.')
        login(request, user)
        messages.success(
            request, 'Du hast deine E-Mail-Adresse bestätigt, dein Account wurde erfolgreich aktiviert.')
        return redirect('index')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'authentication/signup_invalid.html')


def reset(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                subject = 'Setzte das Passwort von deinem TheHaps-Account zurück'
                message = render_to_string('authentication/reset_email.html', {
                    'user': user,
                    'domain': os.environ['LIBERTAS_DOMAIN'],
                    'beta': bool(int(os.environ['LIBERTAS_BETA'])),
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': reset_token.make_token(user),
                })
                user.email_user(subject, message)
                log(user, CHANGE, 'Zurücksetzen des Passworts angefordert, Link gesendet.')
            return redirect('reset_sent')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        form = ResetForm()
    return render(request, 'authentication/reset.html', {'form': form})


def reset_sent(request):
    return render(request, 'authentication/reset_sent.html')


def reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and reset_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                if not user.profile.email_confirmed:
                    user.profile.email_confirmed = True
                    log(user, CHANGE,
                        'E-Mail durch Zurücksetzen des Passworts bestätigt.')
                user.save()
                log(user, CHANGE, 'Passwort zurückgesetzt.')
                return redirect('reset_success')
        else:
            form = SetPasswordForm()
        return render(request, 'authentication/reset_set_password.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'authentication/reset_invalid.html')


def reset_success(request):
    return render(request, 'authentication/reset_success.html')


def account(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    request, username=request.user.username, password=form.cleaned_data['password_old'])
                if user is not None:
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    log(user, CHANGE, 'Passwort vom Benutzer geändert.')
                    messages.success(
                        request, 'Dein Passwort wurde erfolgreich geändert.')
                    login(request, user)
                else:
                    form.add_error('password_old', 'Das Passwort ist falsch.')
        else:
            form = ChangePasswordForm()

        return render(request, 'authentication/account.html', {'form': form})
    else:
        return redirect('signin')


def account_delete(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DeleteAccountForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    request, username=request.user.username, password=form.cleaned_data['password'])
                if user is not None:
                    user.delete()
                    messages.info(
                        request, 'Dein Account wurde erfolgreich gelöscht.')
                    return redirect('index')
                else:
                    form.add_error('password', 'Das Passwort ist falsch.')
        else:
            form = DeleteAccountForm()

        return render(request, 'authentication/account_delete.html', {'form': form})
    else:
        return redirect('signin')
