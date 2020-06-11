import random
import string
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


def generate_id(length=16):
    pool = string.ascii_lowercase + string.digits
    return ''.join(random.choice(pool) for i in range(length))


def generate_code(length=12):
    pool = string.ascii_uppercase + string.digits + string.digits
    return ''.join(random.choice(pool) for i in range(length))


def ausgaben_visible():
    return Ausgabe.objects.filter(
        Q(publish_date__lte=date.today()) | Q(force_visible=True))


def ausgaben_user(user):
    inventory = []
    for ausgabe in ausgaben_visible():
        if ausgabe.access_read(user):
            print("hi")
            inventory.append(ausgabe)
    return inventory


class Ausgabe(models.Model):
    name = models.CharField(max_length=64)
    publish_date = models.DateField('Erscheinungsdatum', blank=True, null=True)
    force_visible = models.BooleanField(
        verbose_name="Sichtbarkeit erzwingen", default=False)
    number = models.IntegerField('Ausgaben-Nr.', primary_key=True)
    file_identifier = models.CharField(
        max_length=16, default=generate_id, unique=True)
    file = models.FileField('Datei', upload_to='ausgaben')
    leseprobe = models.FileField(upload_to='leseproben', blank=True)
    thumbnail = models.FileField(upload_to='thumbnails')

    def __str__(self):
        return "%s (#%s)" % (self.name, self.number)

    class Meta:
        verbose_name = "Ausgabe"
        verbose_name_plural = "Ausgaben"

    # Ist die Ausgabe veröffentlicht?
    def published(self):
        if self.publish_date:
            if date.today() >= self.publish_date:
                return True
        return False

    # Ist die Ausgabe und Leseprobe sichtbar?
    def visible(self):
        if self.force_visible or self.published():
            return True
        return False

    # Ist der Benutzer dazu berechtigt die volle Ausgabe zu lesen?
    def access_read(self, user):
        if user.is_authenticated and self.published():
            if Code.objects.filter(user=user, ausgabe=self).exists():
                return True
        return False

    # Ist der Benutzer dazu berechtigt die Leseprobe zu lesen?
    def access_leseprobe(self, user):
        if user.is_authenticated and self.visible() and self.leseprobe:
            return True
        return False


class Code(models.Model):
    code = models.CharField(
        max_length=12, primary_key=True)
    creation = models.DateTimeField('Erstellung', auto_now_add=True)
    ausgabe = models.ForeignKey(
        Ausgabe, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None,
                             blank=True, null=True, verbose_name='Benutzer')
    redeemed = models.DateTimeField(
        'Zeitpunkt', default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
        super(Code, self).save(*args, **kwargs)

    def __str__(self):
        return "%s****" % (self.code[:-4])

    class Meta:
        verbose_name = "Code"
        verbose_name_plural = "Codes"


class Configuration(models.Model):
    name = models.CharField(
        max_length=16, default="Einstellungen", unique=True)
    wartung_voll = models.BooleanField(
        verbose_name="Wartungsmodus (Voll)", default=False)
    wartung_auth = models.BooleanField(
        verbose_name="Wartungsmodus (Auth)", default=False)
    wartung_signup = models.BooleanField(
        verbose_name="Wartungsmodus (Registrierung)", default=False)
    wartung_viewer = models.BooleanField(
        verbose_name="Wartungsmodus (Viewer)", default=False)

    class Meta:
        verbose_name = "Konfiguration"
        verbose_name_plural = "Konfiguration"

    def __str__(self):
        return "Einstellungen"

    def voll(self):
        if self.wartung_voll:
            return True
        return False

    def auth(self):
        if self.wartung_auth:
            return True
        return False

    def signup(self):
        if self.wartung_signup:
            return True
        return False

    def viewer(self):
        if self.wartung_viewer:
            return True
        return False
