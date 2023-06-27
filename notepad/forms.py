from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

from notepad.models import Notes


class CreatePost(forms.ModelForm):
    class Meta:
        model = Notes

        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': "Don't forget to create a title!"}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Here will be your post'}),
        }
class UploadImage(forms.Form):
    image = forms.ImageField()


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput)
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm your password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class EditUserFormNoPassword(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    username = forms.CharField(label='Username', widget=forms.TextInput)
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput)
    photo = forms.ImageField(label='Photo', widget=forms.FileInput)

    class Meta:
        model = User
        fields = ('username', 'email')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)