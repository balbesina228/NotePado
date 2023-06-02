from django.urls import path

from notepad import views

urlpatterns = [
    path('notes', views.all_notes, name='notes'),
    path('', views.greeting, name='home'),
    path('notes/create_post', views.create_post, name='create_post'),
    path('notes/<id=int>', views.note, name='note')
]
