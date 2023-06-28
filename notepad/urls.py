from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from notepad import views

urlpatterns = [
    path('notes/', views.all_notes, name='notes'),
    path('', views.greeting, name='home'),
    path('notes/create_post', views.create_post, name='create_post'),
    path('notes/<int:note_id>', views.note, name='note'),
    path('notes/<int:note_id>/edit-post', views.edit_post, name='edit-post'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('users/<slug:username>/', views.profile, name='profile'),
    path('users/<slug:username>/edit-profile', views.edit_profile, name='edit-profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)