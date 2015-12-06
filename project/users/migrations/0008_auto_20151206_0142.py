# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151206_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='[0-9]*', message='Это поле может содержать только символы кириллицы.')], max_length=75, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='[0-9]*', message='Это поле может содержать только символы кириллицы.')], max_length=75, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(blank=True, validators=[django.core.validators.RegexValidator(regex='[0-9]*', message='Это поле может содержать только символы кириллицы.')], max_length=75, verbose_name='Отчество'),
        ),
    ]
