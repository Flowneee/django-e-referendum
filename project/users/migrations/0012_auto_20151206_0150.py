# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20151206_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(blank=True, max_length=75, validators=[django.core.validators.RegexValidator(regex='[а-яА-Я]{1,}', message='Это поле может содержать только символы кириллицы.')], verbose_name='Отчество'),
        ),
    ]
