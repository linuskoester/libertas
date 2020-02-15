from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.contrib.auth.models import User

# Register your models here.


def email_confirmed(obj):
    return obj.profile.email_confirmed


email_confirmed.boolean = True
email_confirmed.short_description = 'Bestätigt'


class UserProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


class AccountsUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'is_active', email_confirmed)


admin.site.unregister(User)

admin.site.register(User, AccountsUserAdmin)
