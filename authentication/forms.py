from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
import os
import urllib.request

# Ein Benutzername kann nur aus Klein-, Großbuchstaben und Punkten bestehen
correct_username = RegexValidator(
    r'^[a-zA-Z.]+$',
    'Deine E-Mail-Adresse kann nur aus Kleinbuchstaben und Punkten bestehen, und keine Umlaute enthalten.')

# Vordefiniertes Feld für den Benutzernamen
username_form = forms.CharField(
    label='E-Mail-Adresse',
    widget=forms.TextInput(
        attrs={'class': 'email',
               'style': 'text-transform:lowercase;',
               'placeholder': 'vorname.nachname',
               'autofocus': True
               }),
    max_length=32,
    validators=[correct_username]
)


def checkbetaaccess(cd, self):
    # Überprüfe ob Beta-Server
    if bool(int(os.environ['LIBERTAS_BETA'])):
        gist = "https://gist.githubusercontent.com/CrazyEasy/23319d88bd9d921eb67b530eb633281a/raw/3d62831e60a7d987ac1387871d554e03e2a3f9eb/libertas-beta-tester.txt"  # noqa
        tester = []
        for username in urllib.request.urlopen(gist):
            tester.append(username.decode('utf-8').replace("\n", ""))
        if cd.get('username') not in tester:
            self.add_error('username',
                           "Für diese E-Mail-Adresse ist kein Beta-Zugang freigeschaltet.")


class SignInForm(forms.Form):
    username = username_form
    password = forms.CharField(
        label='Passwort',
        widget=forms.PasswordInput())


class SignUpForm(forms.Form):
    username = username_form
    password = forms.CharField(
        label='Passwort',
        help_text="""Dein Passwort...<ul>
                     <li>muss 8 Zeichen oder mehr haben</li>
                     <li>darf nicht nur aus Zahlen bestehen</li>
                     <li>darf nicht deiner E-Mail-Adresse ähneln</li>
                     <li>darf kein häufig verwendetes sein</li></ul>""",
        widget=forms.PasswordInput(),
        validators=[validate_password])
    password_confirm = forms.CharField(
        label='Passwort bestätigen',
        widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        # Überprüfe ob Passwörter übereinstimmen
        if cd.get('password') != cd.get('password_confirm') and cd.get('password') is not None:
            self.add_error('password_confirm',
                           'Die Passwörter stimmen nicht überein.')
        # Überprüfe ob ein Account existiert, dessen E-Mail BESTÄTIGT ist
        if User.objects.filter(username=cd.get('username')).exists():
            if User.objects.get(username=cd.get('username')).profile.email_confirmed:
                self.add_error('username',
                               """Für diese E-Mail-Adresse existiert bereits ein Account.
                               Versuche dich anzumelden.""")
        # Überprüfe auf Beta-Zugang, nur beim Beta-Server
        checkbetaaccess(cd, self)
        return cd


class ResetForm(forms.Form):
    username = username_form

    def clean(self):
        cd = self.cleaned_data
        # Überprüfe, ob der Account deaktiviert ist
        if User.objects.filter(username=cd.get('username')).exists():
            if not User.objects.get(username=cd.get('username')).is_active:
                self.add_error(None,
                               """Du kannst dein Passwort nicht zurücksetzen,
                                    da dein Account manuell deaktiviert wurde.""")
        # Überprüfe auf Beta-Zugang, nur beim Beta-Server
        checkbetaaccess(cd.get('username'), self)
        return cd


class SetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Neues Passwort',
        help_text="""Dein Passwort...<ul>
                     <li>muss 8 Zeichen oder mehr haben</li>
                     <li>darf nicht nur aus Zahlen bestehen</li>
                     <li>darf nicht deiner E-Mail-Adresse ähneln</li>
                     <li>darf kein häufig verwendetes sein</li></ul>""",
        widget=forms.PasswordInput(attrs={'autofocus': True}),
        validators=[validate_password])
    password_confirm = forms.CharField(
        label='Neues Passwort bestätigen',
        widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        # Überprüfe, ob Passwörter übereinstimmen
        if cd.get('password') != cd.get('password_confirm') and cd.get('password') is not None:
            print(cd.get('password'))
            print(cd.get('password_confirm'))
            self.add_error('password_confirm',
                           'Die Passwörter stimmen nicht überein.')
        return cd


class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(
        label='Aktuelles Passwort',
        help_text='Gib dein aktuelles Passwort ein, um ungewollte Passwortänderungen zu vermeiden.',
        widget=forms.PasswordInput())
    password = forms.CharField(
        label='Neues Passwort',
        help_text="""Dein neues Passwort...<ul>
                     <li>muss 8 Zeichen oder mehr haben</li>
                     <li>darf nicht nur aus Zahlen bestehen</li>
                     <li>darf nicht deiner E-Mail-Adresse ähneln</li>
                     <li>darf kein häufig verwendetes sein</li></ul>""",
        widget=forms.PasswordInput(),
        validators=[validate_password])
    password_confirm = forms.CharField(
        label='Neues Passwort bestätigen',
        widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        # Überprüfe, ob Passwörter übereinstimmen
        if cd.get('password') != cd.get('password_confirm') and cd.get('password') is not None:
            print(cd.get('password'))
            print(cd.get('password_confirm'))
            self.add_error('password_confirm',
                           'Die Passwörter stimmen nicht überein.')
        return cd


class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        label='Dein Passwort',
        help_text='Gib dein aktuelles Passwort ein, um zu bestätigen, dass du deinen Account löschen möchtest.',
        widget=forms.PasswordInput(attrs={'autofocus': True}))
    confirm = forms.BooleanField(
        label='Ich bestätige, dass ich meinen Libertas-Account permanent löschen möchte.')
