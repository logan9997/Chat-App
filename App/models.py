from django.db import models

class Room(models.Model):
    room = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=30)
    capacity = models.IntegerField()


class User(models.Model):
    user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Message(models.Model):
    message = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)