from django.contrib import admin
from django.contrib.auth import admin as auth
from django.utils.translation import ugettext_lazy as _
from django.forms import TextInput, Textarea
from django.db import models
from django.contrib.auth.models import Group

from users.models import User, ProxyGroup
from users.forms import UserChangeForm, UserCreationForm
from referendums.models import Vote, Referendum


class VotesInline(admin.TabularInline):
    model = Vote
    extra = 0
    readonly_fields = ('id', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '50'})},
    }


class ReferendumsInline(admin.TabularInline):
    model = Referendum
    extra = 0
    readonly_fields = ('id', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 35})},
    }


class UserAdmin(auth.UserAdmin):
    fieldsets = (
        (None, {'fields': ('full_name', 'password')}),
        (_('Персональная информация'), {'fields': (
                                            'last_name', 'first_name',
                                            'patronymic', 'email',
                                            'passport_id', 'birth_date',
                                            'address', 'is_approved',
                                            )}),
        (_('Права'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                 'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['full_name']

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.allow_tags = True
    full_name.short_description = _('Полное имя')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('passport_id', 'last_name', 'first_name',
                       'patronymic', 'email', 'birth_date',
                       'is_approved', 'is_staff', 'is_superuser',
                       'address', 'password1', 'password2')},),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('passport_id', 'last_name', 'first_name', 'patronymic',
                    'birth_date', 'is_approved', 'is_staff')
    search_fields = ('passport_id', 'first_name', 'last_name')
    ordering = ('passport_id',)

    inlines = [
        ReferendumsInline,
        VotesInline,
    ]

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(ProxyGroup, auth.GroupAdmin)
