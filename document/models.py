import datetime

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='notes'
    )

    date = models.DateField(null=False, blank=False, default=datetime.date.today)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='notes/files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Like(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

class View(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='views')