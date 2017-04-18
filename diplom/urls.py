from django.conf.urls import url

from . import views
app_name = 'diplom'
urlpatterns = [
    # ex: /diplom/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /diplom/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<tc_id>[0-9]+)/edit/$', views.edit, name='edit'),
    # ex: /diplom/home/
    url(r'^home/$', views.list_projects, name='projects'),
]
