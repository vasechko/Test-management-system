from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth import views as auth_views


app_name = 'diplom'
urlpatterns = [
     url(r'^logout/$', auth_views.logout, {'next_page': 'diplom:login'},  name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},  name='login'),
    # ex: /diplom/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /diplom/5/
    url(r'^(?P<pk>[0-9])/$', login_required(views.DetailView.as_view()), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$',login_required( views.ResultsView.as_view()), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<tc_id>[0-9]+)/edit/$', views.edit, name='edit'),
    # ex: /diplom/home/
    url(r'^home/$', views.list_projects, name='projects'),

    url(r'^home/(?P<tp_id>[0-9]+)/$', views.list_testsuits, name='list_testsuits'),
    url(r'^home/(?P<tp_id>[0-9]+)/testcase/$',login_required( views.IndexView.as_view()), name='index2'),

]
