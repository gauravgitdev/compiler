from django.urls import path
from . import views

urlpatterns = [
    path('', views.editor_view, name='editor'),
]
