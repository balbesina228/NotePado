from django.db import models
from django.urls import reverse


class Notes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def get_title(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note', kwargs={'note_id': self.id})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Notes'
        ordering = ['time_create']