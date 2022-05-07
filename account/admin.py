import imp
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import Account
from .forms import RegistrationForm

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    form = RegistrationForm
    add_form = RegistrationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('email', 'username', 'name', 'is_admin', 'date_joined', 'last_login')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {
            'fields': (
                'username', 'name', 'profile_img',
                'password', 'date_joined', 'last_login'
            )
        }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'password1', 'password2'
            ),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Account, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
