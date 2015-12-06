from django.contrib import admin
from referendums.models import Vote, Referendum
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms import TextInput, Textarea

# Register your models here.


class VoteAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('id', )}),
        (_('Информация о голосе'), {'fields': (
                                            'referendum',
                                            'user',
                                            'result',
                                            'datetime_created',
                                            )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('referendum',
                       'user',
                       'result',)},
        ),
    )

    readonly_fields = ('id', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '50'})},
    }

    list_display = ('id', 'referendum', 'result', 'user', 'datetime_created',)
    search_fields = ('id', 'referendum', 'result', 'user', 'datetime_created',)
    ordering = ('datetime_created',)


class ReferendumAdmin(admin.ModelAdmin):

    def get_title_string(self, obj):
        return str(obj.title)
    get_title_string.allow_tags = True
    get_title_string.short_description = _('Название')

    fieldsets = (
        (None, {'fields': ('id', 'get_title_string',
                           )}),
        (_('Голоса'), {'fields': ('agree_votes_number',
                                  'disagree_votes_number',)}),
        (_('Информация о референдуме'), {'fields': (
                                            'id',
                                            'title',
                                            'question',
                                            'is_over',
                                            'result',
                                            'initiator',
                                            'top_address',
                                            'datetime_created',
                                            )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title',
                       'question',
                       'is_over',
                       'result',
                       'initiator',
                       'top_address',
                       'datetime_created',)},),
    )

    readonly_fields = ('id', 'agree_votes_number',
                       'disagree_votes_number', 'get_title_string')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
    }

    list_display = ('id', 'title', 'is_over',
                    'result', 'initiator', 'datetime_created',
                    'agree_votes_number', 'disagree_votes_number',)
    search_fields = ('id', 'title', 'result', 'initiator', 'datetime_created',
                     'is_over',)
    ordering = ('datetime_created',)


admin.site.register(Vote, VoteAdmin)
admin.site.register(Referendum, ReferendumAdmin)
