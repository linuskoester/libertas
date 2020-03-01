from django.contrib import admin
from .models import Ausgabe

# Register your models here.


class AusgabeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Generell',               {
         'fields': ['name', 'number', 'publish_date']}),
        ('Dateien', {'fields': ['file', 'leseprobe']}),
    ]

    list_display = ('number', 'name', 'publish_date')
    list_filter = ['publish_date']
    list_display_links = ['name']
    ordering = ['-number']


admin.site.register(Ausgabe, AusgabeAdmin)
