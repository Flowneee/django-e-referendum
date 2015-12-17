from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ready/(?P<referendum_pk>[0-9]+)/$',
        make_referendum_ready,
        name='make_referendum_ready'),
    url(r'^create/(?P<referendum_pk>[0-9]+)/' \
        r'(?P<question_pk>[0-9]+)/$',
        add_answer,
        name='create_answer'),
    url(r'^create/(?P<referendum_pk>[0-9]+)/$',
        add_question,
        name='create_question'),
    url(r'^create/$', CreateReferendumView.as_view(),
        name='create_referendum'),
    url(r'^referendum/(?P<referendum_pk>[0-9]+)/' \
        r'(?P<question_pk>[0-9]+)/(?P<answer_pk>[0-9]+)/$',
        add_vote, name='create_vote'),
    url(r'^referendum/(?P<pk>[0-9]+)/$',
        ReferendumDetailView.as_view(), name='details'),
    url(r'^$', IndexView.as_view(), name='index'),
]
