# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20151206_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passport_id',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex='[0-9]{10}', message='Введен некорректный номер паспорта.')], unique=True, verbose_name='Номер и серия паспорта'),
        ),
    ]
