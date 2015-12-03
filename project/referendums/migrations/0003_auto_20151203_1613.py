# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0002_auto_20151201_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referendum',
            name='question',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='referendum',
            name='result',
            field=models.TextField(verbose_name='Итоговое решение', blank=True),
        ),
    ]
