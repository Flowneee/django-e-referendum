from django.views.generic import TemplateView, CreateView
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

import re

from .models import *
from .forms import *
from users.models import User
from project.settings import DEBUG

# Create your views here.


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
        form.instance.initiator = self.request.user
        form.instance.datetime_created = timezone.now()
        form.save()
        return super(CreateReferendumView, self).form_valid(form)


@require_http_methods(['POST', ])
def add_question(request, referendum_pk):
    r = Referendum.objects.get(id=referendum_pk)
    u = User.objects.get(id=request.user.id)
    if (r.initiator != u) or (u.is_staff is not True):
        return redirect('/referendum/{0}'.format(referendum_pk))
    Question.objects.create(
        user=u,
        referendum=r,
        title=request.POST['title'],
        text=request.POST['text'],
        datetime_created=timezone.now()
    )
    return redirect('/referendum/{0}'.format(referendum_pk))


@require_http_methods(['POST', ])
def add_answer(request, referendum_pk, question_pk):
    u = User.objects.get(id=request.user.id)
    r = Referendum.objects.get(id=referendum_pk)
    if (r.initiator != u) or (u.is_staff is not True):
        return redirect('/referendum/{0}'.format(referendum_pk))
    q = Question.objects.get(id=question_pk)
    Answer.objects.create(
        user=u,
        question=q,
        label=request.POST['label'],
        comment=request.POST['comment'],
        style=request.POST['style'],
    )
    return redirect('/referendum/{0}'.format(referendum_pk))


@require_http_methods(['POST', ])
def make_referendum_ready(request, referendum_pk):
    r = Referendum.objects.get(id=referendum_pk)
    if (r.initiator != request.user) or (request.user.is_staff is not True):
        return redirect('/referendum/{0}'.format(referendum_pk))
    r.is_ready = True
    r.save()
    return redirect('/referendum/{0}'.format(referendum_pk))


class CreateAnswerView(CreateView):
    template_name = 'referendums/create_referendum.html'
    model = Referendum
    form = ReferendumForm

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        form.instance.datetime_created = timezone.now()
        form.save()
        return super(CreateReferendumView, self).form_valid(form)


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


methods = ["POST", ]
if DEBUG is True:
    methods += ["GET", ]


@require_http_methods(methods)
def add_vote(request, referendum_pk, question_pk, answer_pk):
    r = Referendum.objects.get(id=referendum_pk)
    u = User.objects.get(id=request.user.id)
    q = Question.objects.get(id=question_pk)
    a = Answer.objects.get(id=answer_pk)
    obj, created = Vote.objects.update_or_create(
        referendum=r,
        user=u,
        question=q,
        defaults={'answer': a},
    )
    return redirect('/referendum/{0}'.format(referendum_pk))


def search_referendums(patterns):
    '''patterns - массив слов'''
    patterns = patterns.split(' ')
    q = Q()
    for i in patterns:
        # workaround for case insensitive search in cyrillic
        if re.match('[а-яА-Я]+', i):
            q = q | Q(title__contains=i) | Q(question__contains=i)
            i = i.lower()
            q = q | Q(title__contains=i) | Q(question__contains=i)
            i = i[0].upper() + i[1:]
            q = q | Q(title__contains=i) | Q(question__contains=i)
        else:
            q = q | Q(title__icontains=i) | Q(question__icontains=i)
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
