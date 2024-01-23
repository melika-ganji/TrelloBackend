from django.contrib.auth.models import User
from django.db import models
from trello import settings


class Board(models.Model):
    title = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin', null=True)

    def __str__(self):
        return self.title


class List(models.Model):
    title = models.CharField(max_length=32)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.title


class Card(models.Model):
    title = models.CharField(max_length=32)
    deadline = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    tag = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return f"{self.title} => {self.tag}"


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def __str__(self):
        return self.text
