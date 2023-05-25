from django.http import HttpResponseNotFound
from django.shortcuts import render

from notepad.models import Notes


def greeting(request):
    return render(request, 'notepad/home.html')

def all_notes(request):
    notes = Notes.objects.all().order_by('time_create')
    context = {
        'notes': notes,
        'title': 'title',
        'content': 'content',
        'time_create': 'time_create',
        'time_update': 'time_update',
        'completed': 'completed'
    }
    return render(request, 'notepad/notes.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found!')
