from djongo import models
from django import forms


class Table(models.Model):
    url = models.URLField()
    num = models.IntegerField()

    def __str__(self):
        return f'<{self.num}>'

    class Meta:
        abstract = True


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'


class Image(models.Model):
    url = models.URLField()
    num = models.IntegerField()

    def __str__(self):
        return f'<Image {self.num}>'

    class Meta:
        abstract = True


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
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
    images = models.ArrayField(
        model_container=Image,
        model_form_class=ImageForm
    )

    def __str__(self):
        return f'<{self.num}>'
    
    class Meta:
        abstract = True


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'


class Document(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    url = models.URLField()
    pages = models.ArrayField(
       model_container=Page,
       model_form_class=PageForm 
    )
    objects = models.DjongoManager()
    
    def __str__(self):
        return f'<{self.name}>'


class ElasticPage(models.Model):
    name = models.CharField(max_length=210, primary_key=True)
    url = models.URLField()
    num = models.IntegerField()
    text = models.TextField()
    doc_name = models.CharField(max_length=200)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return f'<{self.doc_name}-{self.num} {self.pk}>'