from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import  ListView, DetailView
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from .models import *
from .forms import *
from django.db.models import Q
from functools import reduce
import operator
from django.utils import timezone


@login_required
def list_projects(request):
    test_projects = TestProject.objects.all()
    context = {
        'test_projects':test_projects,
    }
    return render(request,"diplom/home.html",context)

class TpCreate(CreateView):
    model = TestProject
    fields = ['name']
    template_name = 'diplom/add.html'

    def form_valid(self, form):
        form.instance.status = ProjectStatus.objects.get(name="Open")#один обьект у модели testProject id кот передается через url
        form.instance.user = self.request.user
        return super(TpCreate, self).form_valid(form)


@login_required
def close_project(request,tp_id):
    project = TestProject.objects.get(pk=tp_id)
    context = {
        'tp_id':tp_id,
        'project':project,
    }
    if request.method=='POST':
        project.status = ProjectStatus.objects.get(name='Closed')
        project.save()
        return redirect('diplom:projects')
    else:
        return render(request,"diplom/close.html", context)


@login_required
def list_testsuits(request,tp_id):
    test_suites = TestSuit.objects.filter(project=tp_id)
    project = TestProject.objects.get(pk=tp_id)
    context = {
        'test_suites':test_suites,
        'tp_id':tp_id,
        'project':project
    }
    return render(request,"diplom/test_suite/list.html",context)

class TsCreate(CreateView):
    model = TestSuit
    fields = ['name', 'description']
    template_name = 'diplom/test_suite/add.html'

    #если нам нужно,чтобы подтягивалось какое то поле не через UI
    def form_valid(self, form):
        form.instance.project = TestProject.objects.get(pk=self.kwargs['tp_id'])#один обьект у модели testProject id кот передается через url
        return super(TsCreate, self).form_valid(form)

    #выбираем те данные котроые будем передавать в качестве контекста шаблону(конечн результат будет формир)
    def get_context_data(self, **kwargs):
        context = super(TsCreate, self).get_context_data(**kwargs)
        context['tp_id'] = self.kwargs['tp_id']
        return context


class TcList(ListView):
    template_name ='diplom/testcase/list.html'
    model=TestCase
    #context_object_name = 'latest_title_list'

    def get_context_data(self, **kwargs):
        context = super(TcList, self).get_context_data(**kwargs)
        context['testSuit'] = get_object_or_404(TestSuit,pk= self.kwargs['ts_id'])#TestSuit.objects.filter(pk = self.kwargs['ts_id'])
        context['project']= get_object_or_404(TestProject,pk= self.kwargs['tp_id'])
        context['test_cases']=TestCase.objects.filter( testSuit = self.kwargs['ts_id'])
        return context

    #def get_queryset(self):
    #    return TestCase.objects.filter( testSuit = self.kwargs['ts_id'])

class TcCreate(CreateView):
    model = TestCase
    fields = ['title', 'priority', 'estimate', 'precondition', 'steps', 'expected_result' ]
    template_name = 'diplom/testcase/add.html'

    def form_valid(self, form):
        form.instance.testSuit = TestSuit.objects.get(pk=self.kwargs['ts_id'])
        return super(TcCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TcCreate, self).get_context_data(**kwargs)
        context['project'] = TestProject.objects.get(pk=self.kwargs['tp_id'])
        return context


class TcUpdate(UpdateView):
    template_name = 'diplom/testcase/edit.html'
    model = TestCase
    fields = ['title', 'priority', 'estimate', 'precondition', 'steps', 'expected_result' ]

    def get_context_data(self, **kwargs):
        context = super(TcUpdate, self).get_context_data(**kwargs)
        context['tp_id'] = self.kwargs['tp_id']
        return context


class TcDelete(DeleteView):
     model = TestCase
     template_name = 'diplom/testcase/delete.html'

     def get_success_url(self):
         return reverse_lazy('diplom:tc-list', kwargs={'tp_id':self.kwargs['tp_id'], 'ts_id':self.kwargs['ts_id']})

     def get_context_data(self, **kwargs):
        context = super(TcDelete, self).get_context_data(**kwargs)
        context['testSuit'] = self.kwargs['ts_id']
        context['project']=  self.kwargs['tp_id']
        context['test_case']=self.kwargs['pk']
        return context

class TcDetail(DetailView):
    model = TestCase
    template_name = 'diplom/testcase/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TcDetail, self).get_context_data(**kwargs)
        context['testSuit'] = self.kwargs['ts_id']
        context['project']=  self.kwargs['tp_id']
        context['test_case']=self.kwargs['pk']
        return context


@login_required
def list_testruns(request,tp_id):
    test_runs = TestRun.objects.filter(testProject=tp_id).order_by("-name")
    project = TestProject.objects.get(pk = tp_id)
    context = {
        'test_runs':test_runs,
        'tp_id':tp_id,
        'project':project
    }
    return render(request,"diplom/testrun/list.html",context)


class TcListSearch(ListView):
    template_name ='diplom/testcase/search-list.html'
    context_object_name = 'test_cases'
    def get_queryset(self):
        result = TestCase.objects.filter(testSuit__project__id = self.kwargs['tp_id'])
        print(len(result))
        query = self.request.GET.get('q')

        if query:
            query_list = query.split()
            print(query_list)
            result = result.filter(
                reduce(operator.and_,
                    (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                    (Q(steps__icontains=q) for q in query_list))
            )
        return result

    def get_context_data(self, **kwargs):
        context = super(TcListSearch, self).get_context_data(**kwargs)
        context['tp_id'] = self.kwargs['tp_id']
        context['search_word'] = self.request.GET.get('q')
        return context


class TrCreate(CreateView):
    model = TestRun
    fields = ['name', 'description', 'testcases' ]
    template_name = 'diplom/testrun/add.html'

    def form_valid(self, form):
        form.instance.testProject = TestProject.objects.get(pk=self.kwargs['tp_id'])
        return super(TrCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TrCreate, self).get_context_data(**kwargs)
        context['tp_id'] = self.kwargs['tp_id']
        return context


class TrDetailList(ListView):
    template_name ='diplom/testrun/tr-detail-list.html'
    context_object_name = 'testrun_testcase'
    #model=TestRun
    def get_queryset(self):
        result = TestRunTestCase.objects.filter(testRun = self.kwargs['tr_id'])
        return result
        #return result.testcases.all()

    def get_context_data(self, **kwargs):
        context = super(TrDetailList, self).get_context_data(**kwargs)
        context['tp_id'] = self.kwargs['tp_id']
        context['tr_id'] = self.kwargs['tr_id']
        context['testRun'] = TestRun.objects.get(pk = self.kwargs['tr_id'])
        return context


class TrrCreate(CreateView):
    model = TestRunResult
    fields = ['status', 'comment' ]
    template_name = 'diplom/testrun/result-add.html'

    def form_valid(self, form):
        form.instance.trrDate = timezone.now()
        form.instance.testrunTestcase = TestRunTestCase.objects.get(testRun=self.kwargs['tr_id'], testCase=self.kwargs['tc_id'])
        form.instance.user = self.request.user
        return super(TrrCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TrrCreate, self).get_context_data(**kwargs)
        context['tp_id'] = self.kwargs['tp_id']
        return context


class TrrDetail(DetailView):
    model = TestCase
    template_name = 'diplom/testrun/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TrrDetail, self).get_context_data(**kwargs)
        context['tr_id'] = self.kwargs['tr_id']
        context['tp_id']=  self.kwargs['tp_id']
        context['tc_id']=self.kwargs['pk']
        context['project']=TestProject.objects.get(pk=context['tp_id'])
        context['testRun']=TestRun.objects.get(pk=context['tr_id'])
        try:
            context['run_result'] = TestRunResult.objects.get(
                testrunTestcase=TestRunTestCase.objects.get(testRun=context['tr_id'],
                                                            testCase= context['tc_id']))
        except TestRunResult.DoesNotExist:
            context['run_result'] = None
        return context

