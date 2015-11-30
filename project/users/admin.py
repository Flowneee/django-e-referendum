from django.contrib import admin
from django.contrib.auth import admin as auth
from django.utils.translation import ugettext_lazy as _

from users.models import User
from users.forms import UserChangeForm, UserCreationForm


class UserAdmin(auth.UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('passport_id', 'password')}),
        (_('Персональная информация'), {'fields': (
                                            'first_name', 'last_name',
                                            'patronymic', 'email',
                                            'passport_id', 'birth_date',
                                            'address'
                                            )}),
        (_('Права'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                 'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('passport_id', 'first_name', 'last_name', 'patronymic',
                    'birth_date', 'is_staff')
    search_fields = ('passport_id', 'first_name', 'last_name')
    ordering = ('passport_id',)

admin.site.register(User, UserAdmin)
