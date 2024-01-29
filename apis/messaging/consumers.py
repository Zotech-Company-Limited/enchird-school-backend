import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apis.messaging.models import *

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self): 
        self.group_name = f"room_{self.scope['url_route']['kwargs']['group_name']}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json
        print(message)

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):

        data = event['message']
        await self.create_message(data=data)

        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):

        get_room_by_name = ChatGroup.objects.get(name=data['group_name'])
        
        if not GroupMessage.objects.filter(content=data['message']).exists():
            new_message = GroupMessage(group=get_room_by_name, sender=data['sender'], content=data['message'])
            new_message.save()  
 
 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self): 
        self.group_name = f"room_{self.scope['url_route']['kwargs']['group_name']}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json
        print(message)

        event = {
            'type': 'send_message',
            'message': message,
        }

        await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):

        data = event['message']
        await self.create_message(data=data)

        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):

        get_room_by_name = ChatGroup.objects.get(name=data['group_name'])
        
        if not GroupMessage.objects.filter(content=data['message']).exists():
            new_message = GroupMessage(group=get_room_by_name, sender=data['sender'], content=data['message'])
            new_message.save()  
 
 
        