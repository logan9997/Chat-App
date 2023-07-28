from django.db import models
from .config import MESSAGE_MAX_LENGTH, NAME_MAX_LENGTH

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    message = models.CharField(max_length=MESSAGE_MAX_LENGTH)
    datetime_sent = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    