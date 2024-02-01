import json
import asyncio
from apis.users.models import User
from apis.messaging.models import *
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer



class GroupChatConsumer(SyncConsumer):
    
    def websocket_connect(self, event): 
        try:
            usr = self.scope['url_route']['kwargs']['user_id']
            group_id = self.scope['url_route']['kwargs']['group_id']
                
            self.group_name = f"group_{group_id}"
            print(self.group_name)
            
            try:
                user = User.objects.get(id=usr, is_deleted=False)
                group = ChatGroup.objects.get(id=group_id)
            except User.DoesNotExist:
                print(f"User with id={usr} not found or is deleted.")
                # async_to_sync(self.close)()
                raise DenyConnection("User not found or is deleted")
            except ChatGroup.DoesNotExist:
                print(f"ChatGroup with id={group_id} not found or is deleted.")
                raise DenyConnection("User not found or is deleted")

            self.send({
                'type': 'websocket.accept'
            }) 
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            print(f'[{self.channel_name}] - You are connected')
            
        except Exception as e:
            print("An error occured:", str(e))
            
    
    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - You are Disconnected')
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        print(event)
        

    def websocket_receive(self, text_data):
        try:
            print(f'[{self.channel_name}] - Received Message - {text_data["text"]}')
            
            # Parse the incoming JSON message
            text_data_json = json.loads(text_data["text"])
            message = text_data_json
            print(text_data_json.get("message"))
            
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "websocket.message",
                    "text": message,
                }
            )
        except Exception as e:
            print("An error occured:", str(e))


    def websocket_message(self, event):
        try:
            print(f'[{self.channel_name}] - Received Sent - {event["text"]}')
            data = event['text']
            
            try:
                get_group_by_name = ChatGroup.objects.get(id=data['group_id'])
                print(get_group_by_name)
                
                new_message = GroupMessage(group=get_group_by_name, sender=data['sender'], content=data['message'])
                new_message.save()
                
                response_data = {
                    'sender': data['sender'],
                    'message': data['message']
                }
                
                self.send({ 
                    "type": "websocket.send",
                    'text': json.dumps(response_data),
                })
            except Exception as e:
                print("An error occurred while processing and sending the message:", str(e))

        except Exception as e:
            print("An error occured:", str(e))
    
 
 
 
class ChatConsumer(AsyncWebsocketConsumer):
    # def websocket__
    async def connect(self): 
        # me = self.scope['user']
        usr = self.scope['url_route']['kwargs']['user_id']
        other_usr = self.scope['url_route']['kwargs']['other_user']
        
        user = User.objects.get(id=usr, is_deleted=False)
        other_user = User.objects.get(id=other_usr, is_deleted=False)
        
        self.group_name = f"thread_{other_user.id}-{user}"
        print(f'[{self.channel_name}] - You are connected')
        
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
        
        if not DirectMessage.objects.filter(content=data['message']).exists():
            new_message = DirectMessage(group=get_room_by_name, sender=data['sender'], content=data['message'])
            new_message.save()  
 
 
        