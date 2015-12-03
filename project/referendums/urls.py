from django.conf.urls import include, url, patterns
from .views import IndexView, CreateReferendumView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$', CreateReferendumView.as_view(), name='create_referendum'),
]