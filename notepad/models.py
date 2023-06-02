from django.db import models


class Notes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def get_title(self):
        return self.title

    def get_data(self):
        return self.title, self.content, self.time_create, self.time_update, self.completed

    def __str__(self):
        return self.time_update.strftime("%d.%m.%Y %H:%M"), self.time_create.strftime("%H:%M")

    class Meta:
        verbose_name_plural = 'Notes'
        ordering = ['time_create']