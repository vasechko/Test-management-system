from django.db import models
from django.urls import reverse

class StatusTestCase (models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name

class ProjectStatus (models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class User (models.Model):
    full_name = models.CharField(max_length=90)
    email_address = models.EmailField(max_length=254)
    password = models.CharField(max_length=90)

    def __str__(self):
        return self.full_name


class Priority(models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class TestProject(models.Model):
    status = models.ForeignKey(ProjectStatus)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=90)
    creation_date = models.DateTimeField()
    modification_date = models.DateTimeField()

    def __str__(self):
        return self.name


class TestSuit (models.Model):
    name = models.CharField(max_length=90)
    description = models.TextField(blank = True)
    project = models.ForeignKey(TestProject)

    def __str__(self):
        return self.name


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
     description = models.TextField()
     testcases = models.ManyToManyField(TestCase)

     def __str__(self):
        return self.name

     def get_absolute_url(self):
        return reverse('diplom:list-testruns', kwargs={'tp_id':self.testProject.pk})


class TestRunResult(models.Model):
   testRun = models.ForeignKey(TestRun)
   testCase = models.ForeignKey(TestCase)
   user = models.ForeignKey(User)
   statusTestCase = models.ForeignKey(StatusTestCase)
   comment = models.CharField(max_length=255)
   trrDATE = models.DateTimeField()

   def __str__(self):
        return self.comment











    #section = models.ForeignKey(Section, on_delete=models.CASCADE)

#class Section(models.Model):
#    name = models.CharField(max_length=100)
#    description = models.TextField()
