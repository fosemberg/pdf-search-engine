from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/?$', views.search),
    url(r'^fast-search/?$', views.search),
    url(r'^upload/?$', views.upload),
    url(r'^all/?$', views.get_all),
]
