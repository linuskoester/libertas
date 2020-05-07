from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from libertas.models import Code
from django.contrib.auth.models import User


def email_confirmed(obj):
    return obj.profile.email_confirmed


email_confirmed.boolean = True
email_confirmed.short_description = 'Bestätigt'


def corona_bestellung(obj):
    return obj.profile.corona_bestellung


corona_bestellung.boolean = True
corona_bestellung.short_description = 'Corona-Bestellung'


class CodeInLine(admin.TabularInline):
    model = Code
    show_change_link = True
    verbose_name_plural = 'Inventar'
    can_delete = False
    min_num = 0
    max_num = 0
    extra = 0
    fields = ['code', 'ausgabe', 'redeemed']


class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False
    verbose_name_plural = 'Profil'


class AccountsUserAdmin(UserAdmin):
    inlines = [UserProfileInline, CodeInLine]
    list_display = ('username', 'email', 'is_active',
                    email_confirmed, corona_bestellung)


admin.site.unregister(User)

admin.site.register(User, AccountsUserAdmin)
