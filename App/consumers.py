import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .config import DATE_SEPERATOR_FORMAT, TIME_FORMAT
from .models import Message
from .utils import format_datetime_sent



class ChatComsumer(WebsocketConsumer):

    active_connections = []
    typing_users = []

    def connect(self):
        self.room_group_name = 'main'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
        if self in self.active_connections:
            self.active_connections.remove(self)



    def receive(self, text_data:str):
        text_data_json = json.loads(text_data)
        print('tdj', text_data_json)
        types = {
            'message_sent': self.send_message,
            'remove_typing_user': self.remove_typing_user,
            'connection_test': self.custom_connect,
            'disconnect': self.custom_disconnect,
            'user_typing':self.user_typing,
            'add_typing_user':self.user_typing,
            'add_all':self.add_all_typing,
            'append_typing_user':self.append_typing_user
        }
        #call function from types dict, pass text_data as parameter.
        types[text_data_json.get('type')](text_data_json)


    def add_all_typing(self, text_data_json):
        print('add_all_typing')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'add_all',
            }
        )  

    def add_all(self, event):
        print('ADD_ALL')
        self.send(text_data=json.dumps({
            'type':'add_all'
        }))


    def async_all_typing(self, text_data_json):
        print('async_all_typing')


        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'connection_test',
                'users':self.typing_users
            }
        )   

    def append_typing_user(self, event):
        name = event.get('name')
        message_input = event.get('message_input')

        typing_users_name = [user['name'] for user in self.typing_users]
        if name not in typing_users_name and message_input != '':
            self.typing_users.append({'name':name, 'message_input':message_input, 'self':self})

        print('TYPING USERS', self.typing_users)

        self.send(text_data=json.dumps({
            'type':'display_all_typing_users',
            'users':[dict(user, **{'self':''}) for user in self.typing_users],
        }))

    def custom_connect(self, text_data_json):
        if self not in self.active_connections:
            self.active_connections.append(self)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'connection_test',
                'name':text_data_json['name'],
            }
        )

    def custom_disconnect(self, text_data_json):
        self.typing_users = [user for user in self.typing_users if user['self'] != self]
        print('DISCONNECT', self.typing_users)
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


