# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20151130_0133'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Суперпользователь', help_text='Обозначает, что пользователь имеет ВСЕ права без явного их указания.')),
                ('first_name', models.CharField(max_length=75, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=75, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=75, verbose_name='Отчество')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='Адрес электронной почты')),
                ('passport_id', models.CharField(unique=True, max_length=10, validators=[django.core.validators.RegexValidator(regex='[0-9]{10}', message='Введен некорректный номер паспорта')], verbose_name='Номер и серия паспорта')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('address', models.TextField(verbose_name='Адрес регистрации')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Администратор', help_text='Обозначает, имеет ли пользователь доступ к администраторской панели.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Обозначает, является ли пользователь активным Вместо удаления аккаунта снимите выбор с этого поля.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_name='user_set', verbose_name='Группы', blank=True, to='auth.Group', help_text='Группы, к которым принадлежит пользователь. Он автоматически получает все права, доступные этой группе.', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(related_name='user_set', verbose_name='Права пользователя', blank=True, to='auth.Permission', help_text='Права, имеющиеся у пользователя.', related_query_name='user')),
            ],
            options={
                'verbose_name_plural': 'Пользователи',
                'verbose_name': 'Пользователь',
            },
        ),
    ]
