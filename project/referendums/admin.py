from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms import TextInput, Textarea

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from referendums.models import Vote, Referendum, Question, Answer

# Register your models here.


class AnswersInline(NestedStackedInline):
    model = Answer
    extra = 0
    readonly_fields = ('id', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 35})},
    }


class QuestionsInline(NestedStackedInline):
    model = Question
    extra = 0
    readonly_fields = ('id', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 35})},
    }

    inlines = [AnswersInline]


class VoteAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('id', )}),
        (_('Информация о голосе'), {'fields': (
                                            'user',
                                            'referendum',
                                            'question',
                                            'answer',
                                            'datetime_created',
                                            )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user',
                       'referendum',
                       'question',
                       'answer',)},
        ),
    )

    readonly_fields = ('id', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '50'})},
    }

    list_display = ('id', 'referendum', 'question', 'answer',
                    'user', 'datetime_created',)
    search_fields = ('id', 'referendum', 'question', 'answer',
                    'user', 'datetime_created',)
    ordering = ('datetime_created',)


class ReferendumAdmin(NestedModelAdmin):

    def get_title_string(self, obj):
        return str(obj.title)
    get_title_string.allow_tags = True
    get_title_string.short_description = _('Название')

    fieldsets = (
        (None, {'fields': ('id', 'get_title_string',
                           )}),
        #(_('Голоса'), {'fields': ('agree_votes_number',
        #                          'disagree_votes_number',)}),
        (_('Информация о референдуме'), {'fields': (
                                            'id',
                                            'title',
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

    inlines = [
        QuestionsInline,
    ]
    readonly_fields = ('id', 'get_title_string')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
    }

    list_display = ('id', 'title', 'is_over',
                    'result', 'initiator', 'datetime_created',)
    search_fields = ('id', 'title', 'result', 'initiator', 'datetime_created',
                     'is_over',)
    ordering = ('datetime_created',)


class QuestionAdmin(NestedModelAdmin):
    inlines = [
        AnswersInline,
    ]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Referendum, ReferendumAdmin)
