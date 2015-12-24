from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ready/(?P<referendum_pk>[0-9]+)/$',
        make_referendum_ready,
        name='make_referendum_ready'),
    url(r'^referendum/mylist/$', MyListView.as_view(),
        name='my_referendums'),
    url(r'^add/$', add, name='add'),
    url(r'^create/$', CreateReferendumView.as_view(),
        name='create_referendum'),
    url(r'^delete/$', delete,  name='delete'),
    url(r'^referendum/(?P<pk>[0-9]+)/$',
        ReferendumDetailView.as_view(), name='details'),
    url(r'^$', IndexView.as_view(), name='index'),
]
