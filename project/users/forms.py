from django.contrib.auth import forms as auth

from users.models import User


class UserCreationForm(auth.UserCreationForm):

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic',
                  'email', 'passport_id', 'birth_date', 'address')


class UserChangeForm(auth.UserChangeForm):

    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = User
        fields = '__all__'
