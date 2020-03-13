from django import forms
from .models import Code


class RedeemForm(forms.Form):
    code = forms.CharField(label='Code',
                           max_length=12,
                           widget=forms.TextInput(
                               attrs={'class': 'code',
                                      'style': 'text-transform:uppercase;',
                                      'autofocus': True
                                      }
                           ))

    def clean(self):
        cd = self.cleaned_data

        if not Code.objects.filter(code=cd.get('code')).exists():
            self.add_error('code', 'Dieser Code ist ungültig.')

        else:
            code = Code.objects.get(code=cd.get('code'))
            if code.user:
                self.add_error('code', 'Dieser Code wurde bereits verwendet.')

        return cd
