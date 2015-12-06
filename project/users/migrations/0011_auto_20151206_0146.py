# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20151206_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='[а-яА-Я]{1,}', message='Это поле может содержать только символы кириллицы.')], verbose_name='Имя', max_length=75),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='[а-яА-Я]{1,}', message='Это поле может содержать только символы кириллицы.')], verbose_name='Фамилия', max_length=75),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='[а-яА-Я]{0,}', message='Это поле может содержать только символы кириллицы.')], blank=True, verbose_name='Отчество', max_length=75),
        ),
    ]
