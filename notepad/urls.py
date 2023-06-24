from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from notepad import views

urlpatterns = [
    path('notes', views.all_notes, name='notes'),
    path('', views.greeting, name='home'),
    path('notes/create_post', views.create_post, name='create_post'),
    path('notes/<int:id>', views.note, name='note')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)