from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.


class Referendum(models.Model):

    title = models.TextField(verbose_name=_('Название'), max_length=200)
    comment = models.TextField(verbose_name=_('Описание'))
    result = models.TextField(verbose_name=_('Итоговое решение'), blank=True)
    initiator = models.ForeignKey(
        'users.User',
        verbose_name=_('Инициатор'),
    )
    top_address = models.TextField(verbose_name=_('Область проведения'))
    datetime_created = models.DateTimeField(
        verbose_name=_('Создан'),
        default=timezone.now
    )
    is_over = models.BooleanField(verbose_name=_('Закончен'), default=False)
    is_ready = models.BooleanField(verbose_name=_('Готов к проверке'),
                                   default=False)
    is_moderated = models.BooleanField(verbose_name=_('Проверен модератором'),
                                       default=False)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return '/referendum/{0}/'.format(self.id)

    def get_short_comment(self):
        if len(str(self.comment)) <= 400:
            return str(self.comment)[0:len(str(self.comment))]
        else:
            return str(self.comment)[0:400]

    @property
    def user(self):
        return self.initiator

    class Meta:

        verbose_name = _('Референдум')
        verbose_name_plural = _('Референдумы')


class Vote(models.Model):

    referendum = models.ForeignKey(
        'Referendum',
        verbose_name=_('Отвечен в'),
        related_name='ref_votes',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('Пользователь'),
        related_name='user_votes',
    )
    question = models.ForeignKey(
        'Question',
        verbose_name=_('Ответ на'),
        related_name='question_votes',
    )
    answer = models.ForeignKey(
        'Answer',
        verbose_name=_('Ответ'),
        related_name='answer_votes',
    )
    datetime_created = models.DateTimeField(
        verbose_name=_('Проголосовал'),
        default=timezone.now
    )

    def __str__(self):
        return str(self.answer)

    def save(self, *args, **kwargs):
        try:
            self.question
        except:
            self.question = self.answer.question
        try:
            self.referendum
        except:
            self.referendum = self.question.referendum
        super(Vote, self).save(*args, **kwargs)

    class Meta:

        verbose_name = _('Голос')
        verbose_name_plural = _('Голоса')

        # голос уникальный для вопроса и юзера
        unique_together = (('question', 'user'),)


class Question(models.Model):

    title = models.TextField(verbose_name=_('Название'), max_length=200)
    text = models.TextField(verbose_name=_('Вопрос'))
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('Автор'),
        related_name='user_questions',
    )
    referendum = models.ForeignKey(
        'Referendum',
        verbose_name=_('Референдум'),
        related_name='referendum_questions',
        on_delete=models.CASCADE,
    )
    datetime_created = models.DateTimeField(
        verbose_name=_('Создан'),
        default=timezone.now
    )

    def get_short_text(self):
        if len(str(self.text)) <= 100:
            return str(self.text)[0:len(str(self.question))]
        else:
            return str(self.text)[0:100]

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')


class Answer(models.Model):

    label = models.CharField(verbose_name=_('Метка'), max_length=50)
    comment = models.TextField(verbose_name=_('Комментарий'))
    STYLE = [
        ('btn-default', _('Обычный')),
        ('btn-primary', _('Основной')),
        ('btn-success', _('Удача')),
        ('btn-info', _('Инфо')),
        ('btn-warning', _('Предупреждение')),
        ('btn-danger', _('Опасность')),
    ]
    style = models.CharField(
        verbose_name=_('Стиль'),
        max_length=12,
        choices=STYLE,
        default='btn-primary',
    )
    question = models.ForeignKey(
        'Question',
        verbose_name=_('Вопрос'),
        related_name='question_answers',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('Автор'),
        related_name='user_answers',
    )

    def __str__(self):
        return self.label

    def get_votes_number(self):
        return len(Vote.objects.filter(answer=self))

    class Meta:

        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')
