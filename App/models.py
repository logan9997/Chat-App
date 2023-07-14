from django.db import models

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    message = models.CharField(max_length=500)
    datetime_sent = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    