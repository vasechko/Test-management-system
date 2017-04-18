from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

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

def edit(request, tc_id):
    tc = get_object_or_404(TestCase, pk=tc_id)
    #tc = testcase.objects.get(pk=request.POST['title'])
    tc.title = request.POST['title']
    tc.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('diplom:results', args=(tc.id,)))


def list_projects(request):
    return HttpResponse(request.user.username)