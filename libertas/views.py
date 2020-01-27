from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm, SignInForm
from .tokens import account_activation_token

# Create your views here.


def index(request):
    return render(request, 'libertas/index.html')


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
                if not user.profile.email_confirmed:
                    form.add_error(
                        'username',
                        """Du musst deine E-Mail-Adresse zuerst bestätigen, um dich anzumelden.
                           Solltest du keine Bestätigungs-Mail erhalten haben, klicke unten auf
                           "Passwort vergessen" und setze dein Passwort zurück. Dadurch wird
                           dein Account aktiviert."""
                    )
                elif not user.is_active:
                    form.add_error(
                        None,
                        'Dein Account wurde manuell deaktiviert.'
                    )
                else:
                    login(request, user)
                    return redirect('index')
            else:
                form.add_error(
                    None,
                    'Der Account existiert nicht oder das Passwort ist falsch!'
                )
    else:
        form = SignInForm()
    return render(request, 'libertas/login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['username'] + '@halepaghen.de'
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Aktiviere deinen Libertas-Account'
            message = render_to_string('libertas/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'libertas/signup.html', {'form': form})


def account_activation_sent(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'libertas/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'libertas/account_activation_invalid.html')
