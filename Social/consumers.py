from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_code=self.scope['url_route']['kwargs']['room_code']
		self.room_group_name='room_%s' %self.room_code
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
			)
		await self.accept()

	
	async def receive(self,text_data):
		print(text_data)
		text_data_json=json.loads(text_data)
		message=text_data_json['message']
		username=text_data_json['username']
		await self.channel_layer.group_send(
			self.room_group_name,
			{
			'type':'run',
			'message':message,
			'username':username,
			})
	async def run(self,event):
		message=event['message']
		username=event['username']
		await self.send(text_data=json.dumps({
			'message':message,
			'username':username,
			}))

	async def disconnect(self):
		await self.channel_layer.group_discard(
		self.room_group_name,self.channel_name
		)
