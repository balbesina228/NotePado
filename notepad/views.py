from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from notepad.forms import CreatePost, UploadImage
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
        'completed': 'completed',
        'image': 'image'
    }
    return render(request, 'notepad/notes.html', context=context)


def create_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('notes')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = CreatePost()
    return render(request, 'notepad/create_post.html', {'form': form})


def note(request):
    context = {

    }
    return render(request, 'notepad/note.html', context=context)
def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found!')
