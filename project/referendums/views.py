from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import *

# Create your views here.


class IndexView(TemplateView):
    template_name = 'referendums/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['ref_list'] = Referendum.objects.all().reverse()
        return context
