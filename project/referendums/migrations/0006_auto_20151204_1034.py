# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0005_auto_20151203_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referendum',
            name='initiator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Инициатор'),
        ),
    ]
