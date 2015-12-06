from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager, Group)
from django.core.validators import *
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


class NameValidator(RegexValidator):
    regex = r'[а-яА-Я]{1,}'
    message = _('Это поле может содержать только символы кириллицы.')


@deconstructible
class BirthDateValidator(object):
    adulthood = 18
    message_too_old = _('Голосовать могут только лица с {0} лет.'.format(adulthood))
    message_future = _('Дата рождения не может быть будущим. Введите корректную дату рождения')

    def __init__(self, adulthood=None, message_too_old=None,
                 message_future=None):
        if adulthood is not None:
            self.adulthood = adulthood
        if message_too_old is not None:
            self.message_too_old = message_too_old
        if message_future is not None:
            self.message_future = message_future

    def __call__(self, value):
        now = timezone.now().date()
        if now < value:
            raise ValidationError(self.message_future)
        if (now.year - value.year) < self.adulthood:
            raise ValidationError(self.message_too_old)

    def __eq__(self, other):
        return (
            self.adulthood == other.adulthood and
            self.message_too_old == other.message_too_old and
            self.message_future == other.message_future
        )


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

    # Персональная информация
    first_name = models.CharField(
        verbose_name=_('Имя'), max_length=75,
        validators=[NameValidator(), ]
    )
    last_name = models.CharField(
        verbose_name=_('Фамилия'), max_length=75,
        validators=[NameValidator(), ]
    )
    patronymic = models.CharField(
        verbose_name=_('Отчество'),
        max_length=75, blank=True,
        validators=[NameValidator(), ]
    )
    email = models.EmailField(
        verbose_name=_('Адрес электронной почты'),
        max_length=254, blank=True,
        validators=[EmailValidator(message=_('Ввелите корректный e-mail.')), ]
    )
    passport_id = models.CharField(
        verbose_name=_('Номер и серия паспорта'),
        validators=[
            RegexValidator(
                regex=r'[0-9]{10}',
                message=_('Введен некорректный номер паспорта.'),
            ),
        ],
        max_length=10,
        unique=True,
    )
    birth_date = models.DateField(
        verbose_name=_('Дата рождения'),
        validators=[BirthDateValidator(), ],
    )
    address = models.TextField(verbose_name=_('Адрес регистрации'))
    is_approved = models.BooleanField(verbose_name=_('Подтвержден'),
                                      default=False)

    # Информация об аккаунте
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

    def __str__(self):
        s = self.get_short_name() + ' ({0})'.format(self.passport_id)
        return s


class ProxyGroup(Group):

    class Meta:
        proxy = True
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural
