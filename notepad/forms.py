from django import forms

from notepad.models import Notes


class CreatePost(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': "Don't forget to create a title!"}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Here will be your post'})
        }