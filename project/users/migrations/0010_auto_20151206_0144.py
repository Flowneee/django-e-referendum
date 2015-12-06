# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20151206_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(verbose_name='Имя', max_length=75, validators=[django.core.validators.RegexValidator(regex='[0-9]{1,}', message='Это поле может содержать только символы кириллицы.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(verbose_name='Фамилия', max_length=75, validators=[django.core.validators.RegexValidator(regex='[0-9]{1,}', message='Это поле может содержать только символы кириллицы.')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(verbose_name='Отчество', max_length=75, validators=[django.core.validators.RegexValidator(regex='[0-9]{0,}', message='Это поле может содержать только символы кириллицы.')], blank=True),
        ),
    ]
