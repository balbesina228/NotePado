from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Notes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_title(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note', kwargs={'note_id': self.id})

    def get_owner_url(self):
        return reverse('profile', kwargs={'username': self.owner})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Notes'
        ordering = ['time_create']


class UserPhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="photos/", default="photos/default.png")

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
