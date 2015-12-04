from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, first_name, last_name, passport_id, birth_date,
                     address, password, is_staff, is_superuser,
                     **extra_fields):
        now = timezone.now()
        if not passport_id:
            raise ValueError('Номер паспорта обязателен.')
        if not first_name:
            raise ValueError('Имя обязательно.')
        if not last_name:
            raise ValueError('Фамилия обязательна.')
        if not birth_date:
            raise ValueError('Дата рождения обязательна.')
        if not address:
            raise ValueError('Адрес обязателен.')

        user = self.model(first_name=first_name, last_name=last_name,
                          passport_id=passport_id, birth_date=birth_date,
                          address=address,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, passport_id, birth_date,
                    address, password=None, **extra_fields):
        return self._create_user(first_name, last_name, passport_id,
                                 birth_date,
                                 address, password, False, False,
                                 **extra_fields)

    def create_superuser(self, passport_id, password, **extra_fields):
        return self._create_user('Чак', 'Норрис', passport_id,
                                 '1940-03-10',
                                 'Ты шо сука, тебе интересно, может тебе с вертухи переебать?',
                                 password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    #Персональная информация
    first_name = models.CharField(verbose_name=_('Имя'), max_length=75)
    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=75)
    patronymic = models.CharField(
        verbose_name=_('Отчество'),
        max_length=75, blank=True
    )
    email = models.EmailField(
        verbose_name=_('Адрес электронной почты'),
        max_length=254, blank=True
    )
    passport_id = models.CharField(
        verbose_name=_('Номер и серия паспорта'),
        validators=[
            RegexValidator(
                regex=r'[0-9]{10}',
                message='Введен некорректный номер паспорта',
            ),
        ],
        max_length=10,
        unique=True,
    )
    birth_date = models.DateField(verbose_name=_('Дата рождения'))
    address = models.TextField(verbose_name=_('Адрес регистрации'))
    is_approved = models.BooleanField(verbose_name=_('Подтвержден'),
                                      default=False)

    #Информация об аккаунте
    is_staff = models.BooleanField(
        verbose_name=_('Администратор'),
        default=False,
        help_text=_('Обозначает, имеет ли пользователь доступ к '
                    'администраторской панели.')
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_('Обозначает, является ли пользователь активным '
                    'Вместо удаления аккаунта снимите выбор с этого поля.')
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Присоединился'),
        default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'passport_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def get_full_name(self):
        full_name = '%s %s %s' % (self.last_name, self.first_name,
                                  self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        short_name = '%s %s.' % (self.last_name, str(self.first_name)[0])
        if (str(self.patronymic) != ''):
            short_name += str(self.patronymic)[0] + '.'
        return short_name.strip()

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
