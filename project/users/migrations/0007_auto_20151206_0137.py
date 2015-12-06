# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_proxygroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Ввелите корректный e-mail.')], blank=True, verbose_name='Адрес электронной почты'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=75, validators=[users.models.NameValidator()], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=75, validators=[users.models.NameValidator()], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(max_length=75, validators=[django.core.validators.RegexValidator(regex='[a-z]*', message='Это поле может содержать только символы кириллицы.')], blank=True, verbose_name='Отчество'),
        ),
    ]
