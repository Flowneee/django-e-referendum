# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0004_auto_20151203_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referendum',
            name='question',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='referendum',
            name='title',
            field=models.TextField(max_length=200, verbose_name='Название'),
        ),
    ]
