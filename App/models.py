from django.db import models

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    message = models.CharField(max_length=150)