from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

from notepad.models import Notes, Comment


class CreatePost(forms.ModelForm):
    class Meta:
        model = Notes

        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Don't forget to create a title!"}),
            'content': forms.Textarea(attrs={'placeholder': 'Here will be your post'}),
        }


class EditPost(forms.ModelForm):
    class Meta:
        model = Notes

        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Don't forget to create a title!"}),
            'content': forms.Textarea(attrs={'placeholder': 'Here will be your post'}),
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


class EditUserForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')

    username = forms.CharField(label='Username', widget=forms.TextInput)
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput, required=False)
    photo = forms.ImageField(label='Photo', widget=forms.FileInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'photo', 'password')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class CreateComment(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Say something about you've read...", 'rows': 3, 'cols': 40}),
        label='New comment'
    )

    class Meta:
        model = Comment
        fields = ('text', )
