from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class StatusTestRun (models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name

class ProjectStatus (models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class TestProject(models.Model):
    status = models.ForeignKey(ProjectStatus)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=90)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diplom:projects')


class TestSuit (models.Model):
    name = models.CharField(max_length=90)
    description = models.TextField(blank = True)
    project = models.ForeignKey(TestProject)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('diplom:list_testsuits', kwargs={'tp_id':self.project.pk})#формиров ссылки при изменении

class TestCase(models.Model):
    testSuit = models.ForeignKey(TestSuit)
    priority = models.ForeignKey(Priority)
    title = models.CharField(max_length=255)
    estimate = models.CharField(max_length=255)
    precondition = models.TextField(blank = True)
    steps = models.TextField()
    expected_result = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('diplom:tc-list', kwargs={'tp_id':self.testSuit.project.pk, 'ts_id':self.testSuit.pk})


class TestRun(models.Model):
     testProject = models.ForeignKey(TestProject)
     name = models.CharField(max_length=90)
     description = models.TextField(blank = True)
     testcases = models.ManyToManyField(TestCase, through='TestRunTestCase', through_fields=('testRun', 'testCase'),)

     def __str__(self):
        return self.name

     def get_absolute_url(self):
        return reverse('diplom:list-testruns', kwargs={'tp_id':self.testProject.pk})


class TestRunTestCase(models.Model):
    testRun = models.ForeignKey(TestRun, on_delete=models.CASCADE)# парам кот указыв все записи буд уд
    testCase = models.ForeignKey(TestCase, on_delete=models.CASCADE)

    class Meta:
        auto_created = True#одновременн изм и Test R и TestCase

class TestRunResult(models.Model):
   testrunTestcase = models.OneToOneField(TestRunTestCase, on_delete=models.CASCADE, primary_key=True,)
   user = models.ForeignKey(User)
   status = models.ForeignKey(StatusTestRun)
   comment = models.CharField(max_length=255,blank = True)
   trrDate = models.DateTimeField()

   def get_absolute_url(self):
        return reverse('diplom:trr-detail', kwargs={'tp_id':self.testrunTestcase.testRun.testProject.pk,#записів ключи
                       'tr_id':self.testrunTestcase.testRun.pk,
                       'pk':self.testrunTestcase.testCase.pk})

   class Meta:
        auto_created = True

   def __str__(self):
        return self.comment
