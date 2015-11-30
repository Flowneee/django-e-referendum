# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Referendum',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('question', models.TextField(verbose_name='Сущность')),
                ('result', models.TextField(verbose_name='Итоговое решение')),
                ('top_address', models.TextField(verbose_name='Область проведения')),
                ('initiator', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='Инициатор')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('result', models.CharField(max_length=1, verbose_name='Ответ', choices=[('y', 'Да'), ('n', 'Нет'), ('u', 'Не знаю')], default='u')),
                ('referendum', models.ForeignKey(to='referendums.Referendum', related_name='ref_votes', verbose_name='Ответ на')),
                ('user', models.ForeignKey(to='referendums.Referendum', related_name='user_votes', on_delete=django.db.models.deletion.PROTECT, verbose_name='Пользователь')),
            ],
        ),
    ]
