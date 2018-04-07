from django.urls import path
from snippets import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^snippets/$', views.snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail, name='snippet-detail'),
    url(r'^users/$', views.user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail, name='user-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.get_snippet_highlight, name='snippet-highlight')
])
