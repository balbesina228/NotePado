from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files import File
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from notepad.forms import CreatePost, RegisterUserForm, LoginUserForm, EditUserForm
from notepad.models import Notes, UserPhoto
from notepad.utils import DataMixin


def greeting(request):
    return render(request, 'notepad/home.html')


def all_notes(request):
    notes = Notes.objects.all().order_by('-time_create')
    context = {
        'notes': notes,
        'title': 'title',
        'owner': 'owner',
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
                new_note = form.save(commit=False)
                new_note.owner = request.user
                new_note.save()
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
        'owner': 'owner',
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
        photo = UserPhoto.objects.create(user=user, photo='photos/default.png')
        photo.save()
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


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    image = get_object_or_404(UserPhoto, user=user.pk)
    context = {
        'username': username,
        'image': image,
        'email': 'email'
    }
    return render(request, 'notepad/profile.html', context=context)


@login_required
def edit_profile(request, username):
    user = request.user
    profile = User.objects.get(username=username)
    image = get_object_or_404(UserPhoto, user=user.pk)
    if str(user) != str(username):
        return page_not_found(request, 404)

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            if form.cleaned_data['photo']:
                new_image = form.cleaned_data['photo']
                image.photo.save(new_image.name, File(new_image))
            else:
                image.photo = image.photo
            return redirect('profile', username=username)

    else:
        form = EditUserForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'notepad/edit-profile.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found!')
