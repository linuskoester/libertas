import os
import urllib.request

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator

# Ein Benutzername kann nur aus Klein-, Großbuchstaben und Punkten bestehen
correct_username = RegexValidator(
    r'^[a-zA-Z.-]+$',
    'Deine E-Mail-Adresse kann nur aus Kleinbuchstaben und Punkten bestehen, und keine Umlaute enthalten.')


def checkbetaaccess(username, self):
    # Überprüfe ob Beta-Server
    if bool(int(os.environ['LIBERTAS_BETA'])) and username:
        gist = "https://gist.githubusercontent.com/CrazyEasy/23319d88bd9d921eb67b530eb633281a/raw/libertas-beta-tester.txt"  # noqa
        tester = []
        for u in urllib.request.urlopen(gist):
            tester.append(u.decode('utf-8').replace("\n", ""))
        if username not in tester:
            print(username, tester)
            self.add_error('username',
                           "Für diese E-Mail-Adresse ist kein Beta-Zugang freigeschaltet.")


class UsernameField(forms.CharField):
    def to_python(self, value):
        return value.lower()


class SignInForm(forms.Form):
    username = UsernameField(
        label='E-Mail-Adresse',
        widget=forms.TextInput(
            attrs={'class': 'email',
                   'style': 'text-transform:lowercase;',
                   'placeholder': 'vorname.nachname',
                   'autofocus': True
                   }),
        max_length=32
    )
    password = forms.CharField(
        label='Passwort',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ))

    def clean(self):
        cd = self.cleaned_data
        user = authenticate(username=cd.get('username'),
                            password=cd.get('password'))
        # Fehlermeldung wenn Authentifizierung fehlgeschlagen
        if user is None:
            self.add_error(
                'username',
                'Der Account existiert nicht oder das Passwort ist falsch!'
            )
        # Fehlermeldung wenn Account deaktiviert
        elif not user.is_active:
            self.add_error(
                None,
                'Dein Account wurde manuell deaktiviert.'
            )
        # Fehlermeldung wenn E-Mail-Adresse nicht bestätigt
        elif not user.profile.email_confirmed:
            self.add_error(
                'username',
                """Du musst deine E-Mail-Adresse zuerst bestätigen, um dich anzumelden.
                    Solltest du keine Bestätigungs-Mail erhalten haben, klicke unten auf
                    "Passwort vergessen" und setze dein Passwort zurück. Dadurch wird
                    dein Account aktiviert."""
            )


class SignUpForm(forms.Form):
    username = UsernameField(
        label='E-Mail-Adresse',
        help_text="""Die digitale Version von TheHaps ist zurzeit ausschließlich für
                     Schülerinnen und Schüler, sowie Lehrkräfte der Halepaghen-Schule
                     verfügbar. Deswegen wird eine gültige IServ-E-Mail-Adresse benötigt.""",
        widget=forms.TextInput(
            attrs={'class': 'email',
                   'style': 'text-transform:lowercase;',
                   'placeholder': 'vorname.nachname',
                   'autofocus': True
                   }),
        max_length=32,
        validators=[correct_username]
    )
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
    confirm1 = forms.BooleanField(
        label="""Ich bin mit den <a href="/agb">Nutzungsbedingungen</a> einverstanden und
                 stimme diesen zu.""")
    confirm2 = forms.BooleanField(
        label="""Ich bin mit der <a href="/datenschutz">Datenschutzerklärung</a> einverstanden
                 und stimme dieser zu.""")

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
        # if bool(int(os.environ['LIBERTAS_BETA'])) and cd.get('username'):
        checkbetaaccess(cd.get('username'), self)
        return cd


class ResetForm(forms.Form):
    username = UsernameField(
        label='E-Mail-Adresse',
        widget=forms.TextInput(
            attrs={'class': 'email',
                   'style': 'text-transform:lowercase;',
                   'placeholder': 'vorname.nachname',
                   'autofocus': True
                   }),
        max_length=32
    )

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
        widget=forms.PasswordInput(attrs={'autofocus': True}))
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
        label="""Ich bin damit einverstanden, dass ich permanent den Zugriff
                 auf alle von mir erworbenen und bezahlten Ausgaben verliere.""",
        help_text='Du hast <b>keinen</b> Anspruch auf Ersatz, solltest du deinen Account aus Versehen löschen.')
    confirm2 = forms.BooleanField(
        label="""Ich möchte meinen Account permanent löschen. Diese Aktion kann
                 nicht rückgängig gemacht werden.""")
