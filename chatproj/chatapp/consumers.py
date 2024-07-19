import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *


def list_to_string(list_):
    string = ""
    rev = list(reversed(list_))
    for l in rev:
        string += f'{l.message} \n'
    return string


class PrivetChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.chat_path = f'/private/{self.room_name}/'
        self.chat = PrivetChat.objects.get(chat_path=self.chat_path)

        list_messages = PrivetMessage.objects.all().filter(chat=self.chat).order_by('-id')[:20]
        res_messages = list_to_string(list_messages)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        if res_messages != '':
            self.send(text_data=json.dumps({"message": res_messages}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        mes = PrivetMessage.objects.create(chat=self.chat, message=message)
        mes.save()

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "chat.message", "message": message})

    def chat_message(self, event):
        message = event["message"]


        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


class PublicChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.chat_path = f'/rooms/{self.room_name}/'
        self.chat = PublicChat.objects.get(slug=self.room_name)

        list_messages = PublicMessage.objects.all().filter(chat=self.chat).order_by('-id')[:20]
        res_messages = list_to_string(list_messages)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        if res_messages != '':
            self.send(text_data=json.dumps({"message": res_messages}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        mes = PublicMessage.objects.create(chat=self.chat, message=message)
        mes.save()

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "chat.message", "message": message})

    def chat_message(self, event):
        message = event["message"]


        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))