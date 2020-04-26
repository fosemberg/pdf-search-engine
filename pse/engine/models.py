from django.db import models

# Create your models here.

class Page(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    url = models.URLField()
    num = models.IntegerField()
    text = models.TextField()


class Document(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
