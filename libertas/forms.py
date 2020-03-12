from django import forms
from .models import Token


class RedeemForm(forms.Form):
    token = forms.CharField(label='Token',
                            max_length=12,
                            min_length=12,
                            widget=forms.TextInput(
                                attrs={'style': 'text-transform:uppercase;',
                                       'autofocus': True
                                       }
                            ))

    def clean(self):
        cd = self.cleaned_data

        if not Token.objects.filter(token=cd.get('token')).exists():
            self.add_error('token', 'Dieser Token ist ungültig.')

        else:
            token = Token.objects.get(token=cd.get('token'))
            if token.user:
                self.add_error('token', 'Dieser Token wurde bereits verwendet.')

        return cd
