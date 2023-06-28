from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files import File
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from notepad.forms import CreatePost, RegisterUserForm, LoginUserForm, EditUserForm, EditPost
from notepad.models import Notes, UserPhoto, Comment
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
        'image': 'image'
    }
    return render(request, 'notepad/notes.html', context=context)


@login_required
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


@login_required
def edit_post(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    if request.user != note.owner:
        raise HttpResponseForbidden
    if request.method == 'POST':
        form = EditPost(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note', note_id=note_id)
    else:
        form = EditPost(instance=note)
    context = {
        'form': form,
        'note_id': note_id
    }
    return render(request, 'notepad/edit_post.html', context=context)


@login_required
def delete_post(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    if request.user != note.owner:
        raise HttpResponseForbidden
    if request.method == "POST":
        note.delete()
        return redirect('notes')
    context = {
        'note': note
    }

    return render(request, 'notepad/delete_post.html', context=context)


def note(request, note_id):
    post = Notes.objects.get(id=note_id)
    comments = Comment.objects.filter(note=post).order_by('-date_added')
    context = {
        'note': post,
        'comments': comments,
        'owner': 'owner',
        'title': 'title',
        'content': 'content',
        'time_create': 'time_create',
        'time_update': 'time_update',
        'image': 'image',
        'photo': 'photo'
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
    notes = Notes.objects.filter(owner=user.id).order_by('-time_update')
    context = {
        'username': username,
        'image': image,
        'notes': notes,
        'email': 'email'
    }
    return render(request, 'notepad/profile.html', context=context)


@login_required
def edit_profile(request, username):
    user = request.user
    profile = User.objects.get(username=username)
    image = get_object_or_404(UserPhoto, user=user.pk)
    if str(user) != str(username):
        raise HttpResponseForbidden

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
    return render(request, 'notepad/edit_profile.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('Page not found!')
