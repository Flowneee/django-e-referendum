from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.contrib.auth import forms as auth
from django.utils.translation import ugettext_lazy as _

from .models import User
from project.settings import LANGUAGE_CODE

from bootstrap3_datetime.widgets import DateTimePicker


# Create your views here.


class UserRegistrationForm(auth.UserCreationForm):
    birth_date = forms.DateField(
        widget=DateTimePicker(options={'format': 'DD.MM.YYYY',
                                       'showTodayButton': True,
                                       'locale': LANGUAGE_CODE}),
        label=_('Дата рождения')
    )

    def __init__(self, *args, **kargs):
        super(UserRegistrationForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic',
                  'email', 'passport_id', 'birth_date', 'address')


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')
