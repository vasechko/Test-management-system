from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import *

from .models import TestCase


class IndexView(generic.ListView):
    template_name = 'diplom/index.html'
    context_object_name = 'latest_title_list'

    def get_queryset(self):
        return TestCase.objects.order_by('-title')[:5]

class DetailView(generic.DetailView):
    model = TestCase
    template_name = 'diplom/detail.html'


class ResultsView(generic.DetailView):
        model = TestCase
        template_name = 'diplom/results.html'

@login_required
def edit(request, tc_id):
    tc = get_object_or_404(TestCase, pk=tc_id)

    #tc = testcase.objects.get(pk=request.POST['title'])
    tc.title = request.POST['title']
    tc.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('diplom:results', args=(tc.id,)))

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




