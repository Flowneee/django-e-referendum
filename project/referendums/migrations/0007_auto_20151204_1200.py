# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0006_auto_20151204_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Создан'),
        ),
        migrations.AddField(
            model_name='vote',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Проголосовал'),
        ),
    ]
