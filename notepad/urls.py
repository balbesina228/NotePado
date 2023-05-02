from django.urls import path

from notepad.views import index

urlpatterns = [
    path('', index)
]
