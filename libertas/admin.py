from django.contrib import admin

from .models import Ausgabe, Code, Configuration, News

# Register your models here.


class AusgabeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Generell',               {
         'fields': ['name', 'number', 'publish_date', 'description', 'force_visible']}),
        ('Dateien', {'fields': ['file', 'leseprobe', 'thumbnail']}),
    ]

    search_fields = ['name', 'number']
    list_display = ('name', 'number', 'publish_date')
    list_filter = ['publish_date']
    list_display_links = ['name']
    ordering = ['-number']


class CodeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,       {'fields': ['code', 'creation', 'ausgabe']}),
        ('Einlösung', {'fields': ['user', 'redeemed']})
    ]

    search_fields = ['code', 'user__username']
    autocomplete_fields = ('ausgabe', 'user')
    list_display = ('censored_code', 'ausgabe', 'creation', 'user', 'redeemed')
    readonly_fields = ['code', 'creation']
    list_filter = ('creation', 'redeemed', 'ausgabe')

    def censored_code(self, obj):
        return "%s****" % (obj.code[:-4])
    censored_code.short_description = 'Code'


class ConfigurationAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name']}),
                 ('Wartung',       {'fields': [
                     'wartung_voll', 'wartung_auth', 'wartung_signup', 'wartung_viewer']})
                 ]

    list_display = ['name']


class NewsAdmin(admin.ModelAdmin):
    ordering = ['-date']
    search_fields = ('tag', 'title', 'author', 'date')
    list_display = ('tag', 'title', 'author', 'date')
    list_display_links = ['title']


admin.site.register(Ausgabe, AusgabeAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(News, NewsAdmin)
