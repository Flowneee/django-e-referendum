# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0003_auto_20151203_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='referendum',
            name='title',
            field=models.TextField(verbose_name='Название', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='referendum',
            name='question',
            field=models.TextField(verbose_name='Содержание', blank=True),
        ),
    ]
