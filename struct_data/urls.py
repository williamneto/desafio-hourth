from django.urls import path

from . import views

urlpatterns = [
    path('(?P<start_date>\w{1,50})', views.index, name='index'),
]