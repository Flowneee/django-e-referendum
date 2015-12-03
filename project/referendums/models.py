from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Referendum(models.Model):

    title = models.TextField(verbose_name=_('Название'), max_length=200)
    question = models.TextField(verbose_name=_('Содержание'))
    result = models.TextField(verbose_name=_('Итоговое решение'), blank=True)
    initiator = models.OneToOneField(
        'users.User',
        verbose_name=_('Инициатор'),
    )
    top_address = models.TextField(verbose_name=_('Область проведения'))

    def __str__(self):
        return str(self.title)

    def get_short_question(self):
        if len(str(self.question)) <= 400:
            return str(self.question)[0:len(str(self.question))]
        else:
            return str(self.question)[0:400]

    class Meta:

        verbose_name = _('Референдум')
        verbose_name_plural = _('Референдумы')


class Vote(models.Model):

    referendum = models.ForeignKey(
        'Referendum',
        verbose_name=_('Ответ на'),
        related_name='ref_votes',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'Referendum',
        verbose_name=_('Пользователь'),
        related_name='user_votes',
        on_delete=models.PROTECT,
    )

    CHOICES = [('y', _('Да')), ('n', _('Нет')), ('u', _('Не знаю'))]
    result = models.CharField(
        verbose_name=_('Ответ'),
        choices=CHOICES,
        default='u',
        max_length=1
    )

    def __str__(self):
        return str(self.result)

    class Meta:

        verbose_name = _('Голос')
        verbose_name_plural = _('Голоса')
