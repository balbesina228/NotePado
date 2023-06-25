from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from notepad.forms import CreatePost, UploadImage, RegisterUserForm, LoginUserForm
from notepad.models import Notes
from notepad.utils import DataMixin


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
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('notes')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = CreatePost()
    return render(request, 'notepad/create_post.html', {'form': form})


def note(request, note_id):
    post = Notes.objects.get(id=note_id)
    context = {
        'note': post,
        'title': 'title',
        'content': 'content',
        'time_create': 'time_create',
        'time_update': 'time_update',
        'completed': 'completed',
        'image': 'image'
    }
    return render(request, 'notepad/note.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'notepad/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Register')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'notepad/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login')

def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found!')
