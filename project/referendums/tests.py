from django.test import TestCase
from .models import Referendum
from .views import search_referendums
from users.models import User

# Create your tests here.


class ReferendumTest(TestCase):

    def test_get_short_question_on_short_question(self):
        '''
        Тестирует возврат первых 400 символов из вопроса на вопросе
        длиной <=400
        '''
        question = 'Another one cool story about ur fckin hard life.'
        title = 'Cool story'
        address = 'Space'
        referendum = Referendum(title=title,
                                question=question, top_address=address)
        self.assertEqual(referendum.get_short_question(), question)

    def test_get_short_question_on_long_question(self):
        '''
        Тестирует возврат первых 400 символов из вопроса на вопросе
        длиной >400
        '''
        question = 'a'
        for i in range(1, 500):
            question += 'a'
        question_assert = 'a'
        for i in range(1, 400):
            question_assert += 'a'
        title = 'Cool story'
        address = 'Space'
        referendum = Referendum(title=title,
                                question=question, top_address=address)
        self.assertEqual(referendum.get_short_question(), question_assert)
