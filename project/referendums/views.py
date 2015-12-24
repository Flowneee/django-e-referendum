from django.views.generic import TemplateView, CreateView
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponseForbidden

import re

from .models import *
from .forms import *
from users.models import User
from project.settings import DEBUG

# Create your views here.


def validate_user(object_user, request_user):
    return (((object_user == request_user) or request_user.is_staff) and
            (request_user.is_staff or request_user.is_approved))


class IndexView(TemplateView):
    template_name = 'referendums/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['ref_list'] = Referendum.objects.filter(is_over=False).\
            exclude(is_moderated=False).order_by('-datetime_created')
        context['ended_ref_list'] = Referendum.objects.filter(is_over=True).\
            exclude(is_moderated=False).order_by('-datetime_created')
        return context


class CreateReferendumView(CreateView):
    template_name = 'referendums/create_referendum.html'
    model = Referendum
    form_class = ReferendumForm

    def form_valid(self, form):
        if not (self.request.user.is_approved or
                self.request.user.is_staff):
            return HttpResponseForbidden()
        form.instance.initiator = self.request.user
        form.instance.datetime_created = timezone.now()
        form.save()
        return super(CreateReferendumView, self).form_valid(form)


def add_question(request):
    r = Referendum.objects.get(id=request.POST['referendum_id'])
    u = User.objects.get(id=request.user.id)
    if not (validate_user(r.initiator, u) and not r.is_ready and
            not r.is_moderated):
        return 403
    Question.objects.create(
        user=u,
        referendum=r,
        title=request.POST['title'],
        text=request.POST['text'],
        datetime_created=timezone.now()
    )
    return 200


def add_answer(request):
    r = Referendum.objects.get(id=request.POST['referendum_id'])
    u = User.objects.get(id=request.user.id)
    if not (validate_user(r.initiator, u) and not r.is_ready and
            not r.is_moderated):
        return 403
    q = Question.objects.get(id=request.POST['question_id'])
    if request.POST.get('style') is None:
        request.POST['style'] = 'btn-primary'
    Answer.objects.create(
        user=u,
        question=q,
        label=request.POST['label'],
        comment=request.POST['comment'],
        style=request.POST['style'],
    )
    return 200


def add_vote(request):
    r = Referendum.objects.get(id=request.POST['referendum_id'])
    u = User.objects.get(id=request.user.id)
    if not (r.is_ready and r.is_moderated and
            (u.is_approved or u.is_staff)):
        return 403
    q = Question.objects.get(id=request.POST['question_id'])
    a = Answer.objects.get(id=request.POST['answer_id'])
    obj, created = Vote.objects.update_or_create(
        referendum=r,
        user=u,
        question=q,
        defaults={'answer': a},
    )
    return 200


@require_http_methods(['POST', ])
def add(request):
    ret_link = '/referendum/{0}'.format(request.POST['referendum_id'])
    type = request.POST['type']
    return_code = 200
    if (type == 'question'):
        return_code = add_question(request)
    if (type == 'answer'):
        return_code = add_answer(request)
    if (type == 'vote'):
        return_code = add_vote(request)
    if (return_code == 200):
        return redirect(ret_link)
    if (return_code == 403):
        return HttpResponseForbidden()


@require_http_methods(['GET', ])
def delete(request):
    type = request.GET['type']
    id = request.GET['id']
    ref = Referendum.objects.get(id=request.GET['referendum_id'])
    object = None
    ret_link = '/referendum/{0}'.format(request.GET['referendum_id'])
    if (type == 'question'):
        object = Question.objects.get(id=id)
    if (type == 'answer'):
        object = Answer.objects.get(id=id)
    if (type == 'referendum'):
        object = ref
        ret_link = '/'
    if not (validate_user(ref.user, request.user) and
            not ref.is_ready and not ref.is_moderated):
        return HttpResponseForbidden()
    object.delete()
    return redirect(ret_link)


@require_http_methods(['POST', ])
def make_referendum_ready(request, referendum_pk):
    r = Referendum.objects.get(id=referendum_pk)
    if (r.initiator != request.user) or (request.user.is_staff is not True):
        return redirect('/referendum/{0}'.format(referendum_pk))
    r.is_ready = True
    r.save()
    return redirect('/referendum/{0}'.format(referendum_pk))


class ReferendumDetailView(TemplateView):
    template_name = 'referendums/details.html'

    def get_context_data(self, **kwargs):
        context = super(ReferendumDetailView, self).get_context_data(**kwargs)
        r = Referendum.objects.get(id=kwargs['pk'])
        q = Question.objects.filter(referendum=r)

        context['referendum'] = r

        if self.request.user != AnonymousUser():
            try:
                context['user_votes'] = self.request.user.user_votes.filter(
                    referendum=context['referendum'],
                )
                context['is_vote'] = True
            except Vote.DoesNotExist:
                context['user_votes'] = None
                context['is_vote'] = False
        if DEBUG:
            print(context)
            print('Вопросы:', r.referendum_questions.all())
            for i in q:
                print('Ответы:', i.question_answers.all())

        if r.is_ready is False:
            context['question_form'] = QuestionForm
            context['answer_form'] = AnswerForm
        else:
            context['question_form'] = None
            context['answer_form'] = None
        return context


def search_referendums(patterns):
    '''patterns - массив слов'''
    patterns = patterns.split(' ')
    q = Q()
    for i in patterns:
        # workaround for case insensitive search in cyrillic
        if re.match('[а-яА-Я]+', i):
            q = q | Q(title__contains=i) | Q(comment__contains=i)
            i = i.lower()
            q = q | Q(title__contains=i) | Q(comment__contains=i)
            i = i[0].upper() + i[1:]
            q = q | Q(title__contains=i) | Q(comment__contains=i)
        else:
            q = q | Q(title__icontains=i) | Q(comment__icontains=i)
    print(q)
    try:
        x = Referendum.objects.filter(q)
    except Referendum.DoesNotExist:
        x = None
    return x


class SearchReferendumView(TemplateView):
    template_name = 'referendums/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchReferendumView, self).get_context_data(**kwargs)
        context['pattern'] = self.request.GET.get('pattern')
        context['ref_list'] = search_referendums(context['pattern'])
        if DEBUG is True:
            print(context['ref_list'])
        return context
