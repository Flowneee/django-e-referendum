from django.test import TestCase, RequestFactory

from .models import *
from .views import *
from users.models import User
from users.bots import *

# Create your tests here.


class ReferendumTest(TestCase):

    def test_get_short_comment_on_short_comment(self):
        '''
        Тестирует возврат первых 400 символов из вопроса на вопросе
        длиной <=400
        '''
        comment = 'Another one cool story about ur fckin hard life.'
        title = 'Cool story'
        address = 'Space'
        referendum = Referendum(title=title,
                                comment=comment, top_address=address)
        self.assertEqual(referendum.get_short_comment(), comment)

    def test_get_short_comment_on_long_comment(self):
        '''
        Тестирует возврат первых 400 символов из вопроса на вопросе
        длиной >400
        '''
        comment = 'a'
        for i in range(1, 500):
            comment += 'a'
        comment_assert = 'a'
        for i in range(1, 400):
            comment_assert += 'a'
        title = 'Cool story'
        address = 'Space'
        referendum = Referendum(title=title,
                                comment=comment, top_address=address)
        self.assertEqual(referendum.get_short_comment(), comment_assert)


class ReferendumViewTest(TestCase):

    def setUp(self):
        self.user = create_bot(1)
        self.referendum = Referendum.objects.create(
            title='Default rederendum', comment='Default comment',
            initiator=self.user, top_address='Default address')
        self.question = Question.objects.create(
            title='Default question', text='Default text',
            user=self.user, referendum=self.referendum)
        self.answer = Answer.objects.create(
            label='Default question', comment='Default comment',
            user=self.user, question=self.question)
        self.factory = RequestFactory()

    def prepare(self, is_ready, is_moderated, is_approved, is_staff):
        self.referendum.is_ready = is_ready
        self.referendum.is_moderated = is_moderated
        self.user.is_approved = is_approved
        self.user.is_staff = is_staff
        self.user.save()
        self.referendum.save()

    def test_create_referendum_view_user_not_approved(self):
        self.prepare(False, False, False, False)
        request = self.factory.post('/create/', {
            'comment': 'Test comment',
            'title': 'Test title',
            'top_address': 'Test address',
        })
        request.user = self.user
        response = CreateReferendumView.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_referendum_view_user_approved(self):
        self.prepare(False, False, True, False)
        request = self.factory.post('/create/', {
            'comment': 'Test comment',
            'title': 'Test title',
            'top_address': 'Test address',
        })
        request.user = self.user
        response = CreateReferendumView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Referendum.objects.all()), 2)

    def test_add_question(self):
        self.prepare(False, False, True, False)
        request = self.factory.post('/add/', {
            'type': 'question',
            'title': 'Test Question title',
            'text': 'Test Question text',
            'referendum_id': str(self.referendum.id),
        })
        request.user = self.user
        response = add(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Question.objects.all()), 2)

    def test_add_answer(self):
        self.prepare(False, False, True, False)
        request = self.factory.post('/add/', {
            'type': 'answer',
            'label': 'Test Answer title',
            'comment': 'Test Answer comment',
            'question_id': str(self.question.id),
            'referendum_id': str(self.referendum.id),
        })
        request.user = self.user
        response = add(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Answer.objects.all()), 2)

    def test_vote_user_not_approved(self):
        self.prepare(False, False, False, False)
        self.user.is_approved = False
        request = self.factory.post('/add/', {
            'type': 'vote',
            'referendum_id': str(self.referendum.id),
            'question_id': str(self.question.id),
            'answer_id': str(self.answer.id),
        })
        request.user = self.user
        response = add(request)
        self.assertEqual(response.status_code, 403)

    def test_vote_user_approved_referendum_isnt_ready(self):
        self.prepare(False, False, True, False)
        self.user.save()
        request = self.factory.post('/add/', {
            'type': 'vote',
            'referendum_id': str(self.referendum.id),
            'question_id': str(self.question.id),
            'answer_id': str(self.answer.id),
        })
        request.user = self.user
        response = add(request)
        self.assertEqual(response.status_code, 403)

    def test_vote_user_approved_referendum_ready(self):
        self.prepare(True, True, True, False)
        request = self.factory.post('/add/', {
            'type': 'vote',
            'referendum_id': str(self.referendum.id),
            'question_id': str(self.question.id),
            'answer_id': str(self.answer.id),
        })
        request.user = self.user
        response = add(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Vote.objects.all()), 1)

    def test_cascade_delete_referendum_from_ready_moderated_referendum(self):
        self.prepare(True, True, True, True)
        request = self.factory.get('/delete/', {
            'type': 'referendum',
            'referendum_id': str(self.referendum.id),
            'id': str(self.referendum.id),
        })
        request.user = self.user
        response = delete(request)
        self.assertEqual(response.status_code, 403)

    def test_cascade_delete_referendum_from_not_ready_not_approved(self):
        self.prepare(False, False, False, False)
        request = self.factory.get('/delete/', {
            'type': 'referendum',
            'referendum_id': str(self.referendum.id),
            'id': str(self.referendum.id),
        })
        request.user = self.user
        response = delete(request)
        self.assertEqual(response.status_code, 403)

    def test_cascade_delete_referendum_from_not_ready_user_approved(self):
        self.prepare(False, False, True, False)
        request = self.factory.get('/delete/', {
            'type': 'referendum',
            'referendum_id': str(self.referendum.id),
            'id': str(self.referendum.id),
        })
        request.user = self.user
        response = delete(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Vote.objects.all()), 0)
        self.assertEqual(len(Answer.objects.all()), 0)
        self.assertEqual(len(Question.objects.all()), 0)
        self.assertEqual(len(Referendum.objects.all()), 0)
