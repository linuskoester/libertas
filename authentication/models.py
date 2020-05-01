from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField('E-Mail bestätigt', default=False)
    notes = models.TextField('Interne Notizen', blank=True, default='')
    ual = models.TextField('User Access Log', blank=True, default='')
    corona_bestellung = models.BooleanField('Corona-Bestellung', default=False)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
