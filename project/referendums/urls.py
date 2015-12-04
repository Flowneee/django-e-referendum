from django.conf.urls import url
from .views import (IndexView, CreateReferendumView, ReferendumDetailView,
                    add_vote)

urlpatterns = [
    url(r'^create/$', CreateReferendumView.as_view(),
        name='create_referendum'),
    url(r'^referendum/(?P<pk>[0-9]+)/(?P<decision>(agree|disagree|idk))/$',
        add_vote, name='create_vote'),
    url(r'^referendum/(?P<pk>[0-9]+)/$',
        ReferendumDetailView.as_view(), name='details'),
    url(r'^$', IndexView.as_view(), name='index'),
]
