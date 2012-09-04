from django.conf.urls import patterns, url

from countries.views import CountryDetailView


urlpatterns = patterns('',
    url(r'^countries/(?P<slug>[\w-]+)/$', CountryDetailView.as_view()),
)
