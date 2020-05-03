from djongo import models
from django import forms


class Table(models.Model):
    url = models.URLField()
    num = models.IntegerField()

    def __str__(self):
        return f'<Table {self.num}>'

    class Meta:
        abstract = True


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'


class Page(models.Model):
    url = models.URLField()
    num = models.IntegerField()
    text = models.TextField()
    vision = models.TextField()
    tables = models.ArrayField(
        model_container=Table,
        model_form_class=TableForm
    )

    def __str__(self):
        return f'<Page {self.num}>'
    
    class Meta:
        abstract = True


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'


class Document(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    pages = models.ArrayField(
       model_container=Page,
       model_form_class=PageForm 
    )
    objects = models.DjongoManager()
    
    def __str__(self):
        return f'<Document {self.name}>'
