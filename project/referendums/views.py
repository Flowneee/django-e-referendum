from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from .models import *
from users.models import User
from project.settings import DEBUG

# Create your views here.


class IndexView(TemplateView):
    template_name = 'referendums/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['ref_list'] = Referendum.objects.all()
        return context


class CreateReferendumView(CreateView):
    template_name = 'referendums/create.html'
    model = Referendum
    fields = ['title', 'question', 'top_address', ]

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        form.instance.datetime_created = timezone.now()
        form.save()
        return super(CreateReferendumView, self).form_valid(form)


class ReferendumDetailView(TemplateView):
    template_name = 'referendums/details.html'

    def get_context_data(self, **kwargs):
        context = super(ReferendumDetailView, self).get_context_data(**kwargs)
        context['referendum'] = Referendum.objects.get(id=kwargs['pk'])
        context['votes'] = Vote.objects.filter(
            referendum=context['referendum'],
        )
        context['for'] = len(context['votes'].filter(result='y'))
        context['against'] = len(context['votes'].filter(result='n'))
        if self.request.user != AnonymousUser():
            try:
                context['user_vote'] = self.request.user.user_votes.get(
                    referendum=context['referendum'],
                )
            except Vote.DoesNotExist:
                context['user_vote'] = None
        if DEBUG:
            print(context)
        return context


@require_http_methods(["POST", ])
def add_vote(request, pk, decision):
    r = Referendum.objects.get(id=pk)
    u = User.objects.get(id=request.user.id)
    a = 'u'
    if (decision == 'agree'):
        a = 'y'
    elif (decision == 'disagree'):
        a = 'n'
    obj, created = Vote.objects.update_or_create(
        referendum=r,
        user=u,
        defaults={'result': a}
    )
    return redirect('/referendum/{0}'.format(pk))

def search_referendums(patterns):
    '''patterns - массив слов'''
    patterns = patterns.split(' ')
    q = Q()
    for i in patterns:
        q = q | Q(title__contains=i) | Q(question__contains=i)
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
        p = self.request.GET.get('pattern')
        context['ref_list'] = search_referendums(p)
        if DEBUG == True:
            print(context['ref_list'])
        return context