from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth import views as auth_views


app_name = 'diplom'
urlpatterns = [
    url(r'^logout/$', auth_views.logout, {'next_page': 'diplom:login'},  name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},  name='login'),
    # ex: /diplom/home/
    url(r'^home/$', views.list_projects, name='projects'),
    url(r'^home/add/$', login_required(views.TpCreate.as_view()), name='tp-add'),
    url(r'^home/close/(?P<tp_id>[0-9]+)/$', views.close_project, name='tp-close'),

    url(r'^home/(?P<tp_id>[0-9]+)/$', views.list_testsuits, name='list_testsuits'),
    url(r'^home/(?P<tp_id>[0-9]+)/testsuit/add/$',login_required(views.TsCreate.as_view()), name='ts-add'),

    url(r'^home/(?P<tp_id>[0-9]+)/(?P<ts_id>[0-9]+)/testcase/$',login_required( views.TcList.as_view()), name='tc-list'),
    url(r'^home/(?P<tp_id>[0-9]+)/(?P<ts_id>[0-9]+)/detail/(?P<pk>[0-9]+)/$', login_required(views.TcDetail.as_view()), name='tc-detail'),
    url(r'^home/(?P<tp_id>[0-9]+)/(?P<ts_id>[0-9]+)/testcase/add/$',login_required( views.TcCreate.as_view()), name='tc-add'),
    url(r'^home/(?P<tp_id>[0-9]+)/(?P<ts_id>[0-9]+)/update/(?P<pk>[0-9]+)/$', login_required(views.TcUpdate.as_view()), name='tc-update'),
    url(r'^home/(?P<tp_id>[0-9]+)/(?P<ts_id>[0-9]+)/delete/(?P<pk>[0-9]+)/$', login_required(views.TcDelete.as_view()), name='tc-delete'),
    url(r'^home/(?P<tp_id>[0-9]+)/testcase/search/$',login_required( views.TcListSearch.as_view()), name='tc-search'),

    url(r'^home/(?P<tp_id>[0-9]+)/testruns/$', views.list_testruns, name='list-testruns'),
    url(r'^home/(?P<tp_id>[0-9]+)/testrun/add/$',login_required( views.TrCreate.as_view()), name='tr-add'),
    url(r'^home/(?P<tp_id>[0-9]+)/(?P<tr_id>[0-9]+)/testrun/$',login_required( views.TrDetailList.as_view()), name='tr-detail-list'),
    url(r'^home/(?P<tp_id>[0-9]+)/(?P<tr_id>[0-9]+)/result/(?P<pk>[0-9]+)/$',login_required( views.TrrDetail.as_view()), name='trr-detail'),
    url(r'^home/(?P<tp_id>[0-9]+)/(?P<tr_id>[0-9]+)/(?P<tc_id>[0-9]+)/result/add/$',login_required( views.TrrCreate.as_view()), name='trr-add'),
]
