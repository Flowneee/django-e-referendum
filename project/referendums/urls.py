from django.conf.urls import include, url, patterns
from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]