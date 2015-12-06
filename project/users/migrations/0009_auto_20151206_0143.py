# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20151206_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(validators=[django.core.validators.RegexValidator(message='Это поле может содержать только символы кириллицы.', regex='[0-9]{1}')], max_length=75, verbose_name='Имя'),
        ),
    ]
