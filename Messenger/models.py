from djongo import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class ChatRoom(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_member')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_member')
    timeCreated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'chat_{self.id}'


class ChatMessage(models.Model):
    chatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    message = models.TextField()
