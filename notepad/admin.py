from django.contrib import admin

from notepad.models import Notes

class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'time_update', 'image')

admin.site.register(Notes, NotesAdmin)
