import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .config import DATE_SEPERATOR_FORMAT, TIME_FORMAT
from .models import Message
from .utils import format_datetime_sent

class Handlers(WebsocketConsumer):

    def send_message_handler(self, event: dict):
        self.send(text_data=json.dumps({
            'type': 'send_message',
            'name': event.get('name'),
            'message': event.get('message'),
            'date_sent': datetime.now().strftime(DATE_SEPERATOR_FORMAT),
            'time_sent': format_datetime_sent(
                datetime.now().strftime(TIME_FORMAT)
            )
        }))

    def add_typing_user_handler(self, event: dict):
        self.send(text_data=json.dumps({
            'type': 'add_typing_user',
            'name': event.get('name'),
        }))

    def remove_typing_user_handler(self, event:dict):
        self.send(text_data=json.dumps({
            'type': 'remove_typing_user',
            'name': event.get('name')
        }))

    def add_all_typing_users_handler(self, event:dict):
        typing_users = list(set(self.typing_users))
        print(typing_users)
        self.send(text_data=json.dumps({
            'type':'add_all_typing_users',
            'typing_users':typing_users
        }))

    def remove_typing_user_on_refresh_handler(self, event:dict):
        name = event.get('name')
        self.send(text_data=json.dumps({
            'type':'remove_typing_user',
            'name':name
        }))

    def create_toast_handler(self, event:dict):
        self.send(text_data=json.dumps({
            'type':'create_toast',
            'name':event.get('name'),
            'connection_type': event.get('connection_type')
        }))


class ChatComsumer(Handlers):

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

    def receive(self, text_data: str):
        text_data_json:dict = json.loads(text_data)
        print('DATA TYPE -', text_data_json.get('type'))
        types = {
            'send_message': self.send_message,
            'add_typing_user': self.add_typing_user,
            'remove_typing_user': self.remove_typing_user,
            'add_all_typing_users': self.add_all_typing_users,
            'remove_typing_user_on_refresh': self.remove_typing_user_on_refresh,
            'create_toast':self.create_toast
        }
        types[text_data_json.get('type')](text_data_json)

    def send_message(self, data: dict):
        name = data.get('name')
        message = data.get('message')
        Message(name=name, message=message).save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'send_message_handler',
                'name': name,
                'message': message,
            }
        )

    def add_typing_user(self, data: dict):
        name = data.get('name')

        self.typing_users.append(name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'add_typing_user_handler',
                'name': name,
            }
        )

    def remove_typing_user(self, data:dict):
        name = data.get('name')
        if name in self.typing_users:
            print(f'REMOVING {name} from typing users')
            self.typing_users.remove(name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'remove_typing_user_handler',
                'name': name,
            }
        )

    def add_all_typing_users(self, data:dict):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'add_all_typing_users_handler',
                'name':data.get('name')
            }
        )

    def remove_typing_user_on_refresh(self, data:dict):
        name = data.get('name')
        if name in self.typing_users:
            print(f'REMOVING {name} from typing users')
            self.typing_users.remove(name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'remove_typing_user_on_refresh_handler',
                'name':name
            }
        )

    def create_toast(self, data:dict):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': 'create_toast_handler',
                'name':data.get('name'),
                'connection_type':data.get('connection_type')
            }
        )    