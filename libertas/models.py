from django.db import models
import string
import random


def generate_id(length=16):
    pool = string.ascii_lowercase + string.digits
    return ''.join(random.choice(pool) for i in range(length))


class Ausgabe(models.Model):
    name = models.CharField(max_length=64)
    publish_date = models.DateField('Erscheinungsdatum', blank=True, null=True)
    number = models.IntegerField('Ausgabennummer', primary_key=True)
    file_identifier = models.CharField(max_length=16, default=generate_id, unique=True)
    file = models.FileField('Datei', upload_to='ausgaben')
    leseprobe = models.FileField(upload_to='leseproben', blank=True)

    def __str__(self):
        return "%s (%s)" % (self.number, self.file_identifier)

    class Meta:
        verbose_name = "Ausgabe"
        verbose_name_plural = "Ausgaben"
