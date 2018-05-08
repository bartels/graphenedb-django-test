from django.conf.urls import url
from django.views.generic import TemplateView

from graphtest.api import views as api_views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),

    # API Urls
    url('^api/neo4j-driver/?$', api_views.neo4j_driver_view),
    url('^api/py2neo/?$', api_views.py2neo_view),
]
