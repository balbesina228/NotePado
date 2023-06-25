from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from notepad import views
from notepad.views import RegisterUser

urlpatterns = [
    path('notes/', views.all_notes, name='notes'),
    path('', views.greeting, name='home'),
    path('notes/create_post', views.create_post, name='create_post'),
    path('notes/<int:note_id>', views.note, name='note'),
    path('login/', views.login, name='login'),
    path('register/', RegisterUser.as_view(), name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)