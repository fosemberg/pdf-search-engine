from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^slow-search/?$', views.slow_search),
    url(r'^fast-search/?$', views.fast_search)
]
