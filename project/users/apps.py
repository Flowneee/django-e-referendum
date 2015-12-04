from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.apps as auth_apps


class UsersConfig(AppConfig):

    name = 'users'
    verbose_name = auth_apps.AuthConfig.verbose_name