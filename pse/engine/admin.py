from django.contrib import admin

from .models import Page, Document

# Register your models here.

class PageInline(admin.StackedInline):
    model = Page
    extra = 5

class DocumentAdmin(admin.ModelAdmin):
    inlines = [PageInline]

admin.site.register(Page)
admin.site.register(Document, DocumentAdmin)
