from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import  ListView, DetailView
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from .models import *
from .forms import *
from django.db.models import Q
from functools import reduce
import operator

from .models import TestCase


class IndexView(ListView):
    template_name = 'diplom/index.html'
    context_object_name = 'latest_title_list'

    def get_queryset(self):
        return TestCase.objects.order_by('-title')[:5]

class DetailView(DetailView):
    model = TestCase
    template_name = 'diplom/detail.html'


class ResultsView(DetailView):
        model = TestCase
        template_name = 'diplom/results.html'

@login_required
def list_projects(request):
    test_projects = TestProject.objects.all()
    context = {
        'test_projects':test_projects,
    }
    return render(request,"diplom/home.html",context)

@login_required
def list_testsuits(request,tp_id):
    test_suites = TestSuit.objects.filter(project=tp_id)
    context = {
        'test_suites':test_suites,
        'tp_id':tp_id
    }

    return render(request,"diplom/test_suite/list.html",context)

@login_required
def edit1(request,tc_id):
    tc = get_object_or_404(TestCase,pk=tc_id)
    form = TestCaseForm
    context = {
        'tc' : tc,
        'form':form,
    }
    return  render(request,"diplom/testcase/edit.html", context)

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
    test_runs = TestRun.objects.filter(testProject=tp_id)
    context = {
        'test_runs':test_runs,
        'tp_id':tp_id
    }
    return render(request,"diplom/testrun/list.html",context)


class TcListSearch(ListView):
    template_name ='diplom/testcase/search-list.html'
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
    context_object_name = 'test_cases'
    #model=TestRun
    def get_queryset(self):
        result = TestRun.objects.get(pk = self.kwargs['tr_id'])
        return result.testcases.all()

    def get_context_data(self, **kwargs):
        context = super(TrDetailList, self).get_context_data(**kwargs)
        context['tp_id'] = self.kwargs['tp_id']
        return context