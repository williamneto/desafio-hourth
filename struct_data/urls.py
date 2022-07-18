from django.urls import path

from . import views

urlpatterns = [
    path('api/', views.api, name='api'),
    path('table/', views.table, name='table')
]