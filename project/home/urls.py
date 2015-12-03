from django.conf.urls import patterns, include, url
from .views import helloworld
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', helloworld, name='index'),
]
