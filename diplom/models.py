from django.db import models

class TestCase(models.Model):
    title = models.CharField(max_length=90)
    steps = models.TextField()
    expected_result = models.TextField()
    #section = models.ForeignKey(Section, on_delete=models.CASCADE)

#class Section(models.Model):
#    name = models.CharField(max_length=100)
#    description = models.TextField()
