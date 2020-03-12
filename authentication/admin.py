from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from libertas.models import Token
from django.contrib.auth.models import User


def email_confirmed(obj):
    return obj.profile.email_confirmed


email_confirmed.boolean = True
email_confirmed.short_description = 'Bestätigt'


class TokenInline(admin.TabularInline):
    model = Token
    show_change_link = True
    verbose_name_plural = 'Inventar'
    can_delete = False
    min_num = 0
    max_num = 0
    extra = 0
    fields = ['ausgabe', 'redeemed']
    readonly_fields = ['ausgabe', 'redeemed']


class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False
    verbose_name_plural = 'Profil'


class AccountsUserAdmin(UserAdmin):
    inlines = [UserProfileInline, TokenInline]
    list_display = ('username', 'email', 'is_active', email_confirmed)


admin.site.unregister(User)

admin.site.register(User, AccountsUserAdmin)
