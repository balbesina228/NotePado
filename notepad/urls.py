from django.urls import path

from notepad import views

urlpatterns = [
    path('notes', views.all_notes, name='notes'),
    path('', views.greeting, name='home')
]
