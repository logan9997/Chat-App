from channels.generic.websocket import WebsocketConsumer
import json
from datetime import datetime
from asgiref.sync import async_to_sync
from .models import Message

DATE_FORMAT = '%B %d, %Y, %I:%M %p'

class ChatComsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data:str):
        text_data_json = json.loads(text_data)
        print('RECIEVE, json (type) - ', text_data_json['type'])
        if text_data_json.get('type') == 'message_sent':
            self.send_message(text_data_json)
        elif text_data_json.get('type') == 'remove_typing_user':
            self.remove_typing_user(text_data_json)
        elif text_data_json.get('type') == 'connection_test':
            self.custom_connect(text_data_json)
        elif text_data_json.get('type') == 'disconnect':
            self.custom_disconnect(text_data_json)
        else:
            self.user_typing(text_data_json)

    def custom_connect(self, text_data_json):
        print('CUSTOM CONNECT')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'connection_test',
                'name':text_data_json['name']
            }
        )

    def custom_disconnect(self, text_data_json):
          async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type':'disconnect_text',
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
        message = event['message']
        name = event['name']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'name': name,
            'datetime_sent':format_datetime_sent(
                datetime.now().strftime(DATE_FORMAT)
            )       
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

    def disconnect_text(self, event):
        self.send(text_data=json.dumps({
            'type':'disconnect',
            'name':event['name']
        }))


def format_datetime_sent(datetime_sent):
    #remove 0 padded hour
    datetime_sent = list(datetime_sent)
    colon_index = datetime_sent.index(':') 
    if datetime_sent[colon_index-2] == '0':
        datetime_sent.pop(colon_index -2)
    datetime_sent = ''.join(datetime_sent)

    if 'AM' in datetime_sent:
        datetime_sent = datetime_sent.replace('AM', 'a.m.')
    else:
        datetime_sent = datetime_sent.replace('PM', 'p.m.')
    return datetime_sent