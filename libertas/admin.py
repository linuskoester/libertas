from django.contrib import admin
from .models import Ausgabe, Token

# Register your models here.


class AusgabeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Generell',               {
         'fields': ['name', 'number', 'publish_date']}),
        ('Dateien', {'fields': ['file', 'leseprobe']}),
    ]

    search_fields = ['name', 'number']
    list_display = ('name', 'number', 'publish_date')
    list_filter = ['publish_date']
    list_display_links = ['name']
    ordering = ['-number']


class TokenAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,       {'fields': ['token', 'creation', 'ausgabe']}),
        ('Benutzer', {'fields': ['user', 'redeemed']})
    ]

    search_fields = ['token', 'user__username']
    autocomplete_fields = ('ausgabe', 'user')
    list_display = ('censored_token', 'ausgabe', 'user', 'redeemed')
    readonly_fields = ['token', 'creation']

    def censored_token(self, obj):
        return "%s****" % (obj.token[:-4])
    censored_token.short_description = 'Token'


admin.site.register(Ausgabe, AusgabeAdmin)
admin.site.register(Token, TokenAdmin)
