from django.db import models

class ChatRoom(models.Model):
    room = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=30)
    capacity = models.IntegerField()


class User(models.Model):
    user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)