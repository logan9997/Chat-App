from django.db import models
from .config import MESSAGE_MAX_LENGTH, NAME_MAX_LENGTH

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    message = models.CharField(max_length=MESSAGE_MAX_LENGTH)
    date_sent = models.DateField(auto_now_add=True, null=True, blank=True)
    time_sent = models.TimeField(auto_now_add=True, null=True, blank=True)