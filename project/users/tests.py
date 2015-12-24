from django.test import TestCase
# Create your tests here.


class UserViewTest(TestCase):

    def test_user_create_view(self):
        self.assertEqual(self.client.post('/register/', {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'email': 'mail@mail.ru',
            'passport_id': '0000000000',
            'birth_date': '01.01.1970',
            'address': 'Адрес',
            'password1': '123123123',
            'password2': '123123123',
        }, follow=True).status_code, 200)
