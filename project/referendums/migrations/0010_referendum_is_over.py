# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0009_auto_20151206_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='is_over',
            field=models.BooleanField(default=False, verbose_name='Закончен'),
        ),
    ]
