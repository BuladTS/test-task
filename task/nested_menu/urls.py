from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.initial, name='initial'),
    path('<path:address>', views.menu, name='menu'),
]
