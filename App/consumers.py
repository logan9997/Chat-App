import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .config import DATE_SEPERATOR_FORMAT, TIME_FORMAT
from .models import Message

active_connections = []

class ChatComsumer(WebsocketConsumer):

    # async_to_sync

    def connect(self):
        self.room_group_name = 'main'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        name = self.scope['session']['name']
        if name not in active_connections:
            active_connections.append(name)
        
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
        name = self.scope['session']['name']
        if name in active_connections:
            active_connections.remove(name)   

    def receive(self, text_data:str):
        text_data_json = json.loads(text_data)
        types = {
            'message_sent': self.send_message,
            'remove_typing_user': self.remove_typing_user,
            'connection_test': self.custom_connect,
            'disconnect': self.custom_disconnect,
            'user_typing':self.user_typing,
            'add_typing_user':self.user_typing
        }
        #call function from types dict, pass text_data as parameter.
        types[text_data_json.get('type')](text_data_json)


    def custom_connect(self, text_data_json):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'connection_test',
                'name':text_data_json['name']
            }
        )

    def custom_disconnect(self, text_data_json):
          async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'disconnect_test',
                'name':text_data_json['name']
            }
        )       

    def remove_typing_user(self, text_data_json):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'remove_typing_user_test',
                'name':text_data_json['name']
            }
        )       

    def send_message(self, text_data_json):
        message = text_data_json['message']
        name = text_data_json['name']

        self.new_message = Message(message=message, name=name)
        self.new_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'chat_message',
                'message': message,
                'name': name,
            }
        )

    def user_typing(self, text_data_json):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'add_typing_user',
                'name':text_data_json['name'],
                'msg_len':text_data_json['msg_len']
            }
        )

    def add_all_typing_users(self, text_data_json):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'add_typing_user',
                'name':text_data_json['name'],
                'msg_len':text_data_json['msg_len']
            }
        )
        
    #json dumps

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':event['message'],
            'name': event['name'],
            'time_sent':format_datetime_sent(
                datetime.now().strftime(TIME_FORMAT)
            ),
            'date_sent':datetime.now().strftime(DATE_SEPERATOR_FORMAT)
        }))

    def add_typing_user(self, event):
        self.send(text_data=json.dumps({
            'type':'add_typing_user',
            'name':event['name'],
            'msg_len':event['msg_len']
        }))

    def remove_typing_user_test(self, event):
        self.send(text_data=json.dumps({
            'type':'remove_typing_user',
            'name':event['name']
        }))

    
    def connection_test(self, event):
        self.send(text_data=json.dumps({
            'type':'new_connection',
            'name':event['name']
        }))

    def disconnect_test(self, event):
        self.send(text_data=json.dumps({
            'type':'disconnect',
            'name':event['name']
        }))


def format_datetime_sent(time_sent:str):
    #remove 0 padded hour
    if time_sent[0] == '0':
        time_sent = time_sent[1:]

    if 'AM' in time_sent:
        time_sent = time_sent.replace('AM', 'a.m.')
    else:
        time_sent = time_sent.replace('PM', 'p.m.')
    return time_sent