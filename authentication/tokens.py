import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SignupTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed) +
            six.text_type(user.password)
        )


signup_token = SignupTokenGenerator()
reset_token = PasswordResetTokenGenerator()
