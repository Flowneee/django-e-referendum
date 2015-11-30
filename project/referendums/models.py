from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Referendum (models.Model):

	question = models.TextField(verbose_name=_('Сущность'))
	answer = models.BooleanField(verbose_name=_())