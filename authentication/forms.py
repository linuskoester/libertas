from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

correct_username = RegexValidator(
    r'^[a-zA-Z.]+$',
    'Deine E-Mail-Adresse kann nur aus Kleinbuchstaben und Punkten bestehen, und keine Umlaute enthalten.')

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
        if cd.get('password') != cd.get('password_confirm') and cd.get('password') is not None:
            self.add_error('password_confirm',
                           'Die Passwörter stimmen nicht überein.')
        if User.objects.filter(username=cd.get('username')).exists():
            if User.objects.get(username=cd.get('username')).profile.email_confirmed:
                self.add_error('username',
                               """Für diese E-Mail-Adresse existiert bereits ein Account.
                               Versuche dich anzumelden.""")
        return cd


class ResetForm(forms.Form):
    username = username_form

    def clean(self):
        cd = self.cleaned_data
        if not User.objects.get(username=cd.get('username')).is_active:
            self.add_error(None,
                           """Du kannst dein Passwort nicht zurücksetzen,
                              da dein Account manuell deaktiviert wurde.""")


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