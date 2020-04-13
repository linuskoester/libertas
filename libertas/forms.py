from django import forms
from .models import Code


class RedeemForm(forms.Form):
    code = forms.CharField(label='Zugangscode einlösen',
                           max_length=12,
                           widget=forms.TextInput(
                               attrs={'class': 'code',
                                      'style': 'text-transform:uppercase;',
                                      'autofocus': True
                                      }
                           ))
    confirm1 = forms.BooleanField(
        label="""Mir ist bewusst, dass jegliche Form der digitalen Vervielfältigung oder des Missbrauchs strafbar
                 ist, und zurückverfolgt werden kann.""",
        help_text="""Wir behalten uns es vor Accounts umgehend zu sperren, welche gegen unsere Nutzungsbedingungen verstoßen.
                     Es besteht kein Anspruch auf Rückerstattung oder Zugriff auf die erworbenen Ausgaben.""")
    confirm2 = forms.BooleanField(
        label="""Ich möchte sofortigen Zugriff auf die Ausgabe, deswegen verzichte
                 ich auf mein 14-tägiges Widerrufsrecht.""")

    def clean(self):
        cd = self.cleaned_data

        if not Code.objects.filter(code=cd.get('code')).exists():
            self.add_error('code', 'Dieser Zugangscode ist ungültig.')

        else:
            code = Code.objects.get(code=cd.get('code'))
            if code.user:
                self.add_error(
                    'code', 'Dieser Zugangscode wurde bereits verwendet.')

        return cd
