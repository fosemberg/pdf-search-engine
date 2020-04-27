from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('slow-search/', views.slow_search),
    path('fast-search/', views.fast_search)
]
