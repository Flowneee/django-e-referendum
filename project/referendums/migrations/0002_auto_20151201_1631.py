# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referendums', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referendum',
            options={'verbose_name_plural': 'Референдумы', 'verbose_name': 'Референдум'},
        ),
        migrations.AlterModelOptions(
            name='vote',
            options={'verbose_name_plural': 'Голоса', 'verbose_name': 'Голос'},
        ),
    ]
