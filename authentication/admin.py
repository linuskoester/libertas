from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from libertas.models import Code
from django.contrib.auth.models import User


def email_confirmed(obj):
    return obj.profile.email_confirmed


email_confirmed.boolean = True
email_confirmed.short_description = 'Bestätigt'


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
    list_display = ('username', 'email', 'is_active', email_confirmed)


admin.site.unregister(User)

admin.site.register(User, AccountsUserAdmin)
