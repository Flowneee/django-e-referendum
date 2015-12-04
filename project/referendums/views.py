from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from .models import *
from users.models import User
from django.utils import timezone

# Create your views here.


class IndexView(TemplateView):
    template_name = 'referendums/referendum_short.html'

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
        context['object'] = Referendum.objects.get(id=kwargs['pk'])
        context['votes'] = Vote.objects.filter(referendum=context['object'])
        context['for'] = len(context['votes'].filter(result='y'))
        context['against'] = len(context['votes'].filter(result='n'))
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
    v = Vote(referendum=r, user=u, result=a)
    v.save()
    return redirect('/referendum/{0}'.format(pk))
