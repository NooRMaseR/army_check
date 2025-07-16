from .models import ArmyPerson, Branch, PendingRequest, Rank, RequestStatus
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from utils.validators import RequestActionModel, RequestModel
from django.db.utils import IntegrityError
import asyncio

REQUEST_GROUP_NAME = "request_group"
MANAGER_GROUP_NAME = "manager_group"

class RequestConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(REQUEST_GROUP_NAME, self.channel_name) # type: ignore
        await self.accept()
        
    async def receive_json(self, content: dict, **kwargs):
        try:
            validated_data = RequestModel(**content)
        except:
            return
        
        (branch, _), (rank, _) = await asyncio.gather(
            Branch.objects.aget_or_create(name=validated_data.branch),
            Rank.objects.aget_or_create(name=validated_data.rank)
        )
        
        
        try:
            army_person, created = await ArmyPerson.objects.select_related("rank", "branch").aget_or_create(
                name = validated_data.name,
                code = validated_data.code,
                rank = rank,
                branch = branch,
            )
            REQUEST, req_created = await PendingRequest.objects.aget_or_create(user=army_person)
            
            if not req_created:
                REQUEST.accepted = RequestStatus.PENDING
                await REQUEST.asave()
                
            match (validated_data.type):
                case "request":
                    await self.channel_layer.group_send( # type: ignore
                        REQUEST_GROUP_NAME, 
                        {
                            "type": "send.request",
                            "name": army_person.name,
                            "code": army_person.code,
                            "rank": army_person.rank.name,
                            "branch": army_person.branch.name,
                            "created": created,
                            "request": {
                                "accepted": REQUEST.accepted
                            }
                        }
                    )
                
                case "pre_request":
                    await self.channel_layer.group_send( # type: ignore
                        REQUEST_GROUP_NAME, 
                        {
                            "type": "send.pre.request",
                            "code": army_person.code,
                            "request": {
                                "accepted": REQUEST.accepted
                            }
                        }
                    )
        except IntegrityError:
            await self.channel_layer.group_send( # type: ignore
                REQUEST_GROUP_NAME, 
                {
                    "type": "send.request.error",
                    "message": "هذا الطلب موجود بالفعل"
                }
            )
        
        
    async def send_request(self, event: dict[str, str]):
        await self.send_json(event)
    
    async def send_pre_request(self, event: dict[str, str]):
        await self.send_json(event)
    
    async def send_request_error(self, event: dict[str, str]):
        await self.send_json(event)


class ActionConsumer(AsyncJsonWebsocketConsumer):
    
    async def receive_json(self, content: dict, **kwargs):
        try:
            validated_data = RequestActionModel(**content)
        except:
            return
        
        army_person = await ArmyPerson.objects.aget(code = validated_data.code)
        
        await PendingRequest.objects.aupdate(action = RequestStatus.ACCEPTED if validated_data.action_response else RequestStatus.REJECTED, defaults={"user": army_person})
        await self.channel_layer.group_send( # type: ignore
            REQUEST_GROUP_NAME, 
            {
                "type": "send.action",
                "code": army_person.code,
                "accepted": validated_data.action_response
            }
        )
        
    async def send_action(self, event: dict[str, str]):
        await self.send_json(event)


class ManagerConsumer(AsyncJsonWebsocketConsumer):
    
    async def receive_json(self, content: dict, **kwargs):
        try:
            validated_data = RequestActionModel(**content)
        except:
            return
        
        army_person = await ArmyPerson.objects.aget(code = validated_data.code)
        
        await PendingRequest.objects.aupdate(action = RequestStatus.ACCEPTED if validated_data.action_response else RequestStatus.REJECTED, defaults={"user": army_person})
        await self.channel_layer.group_send( # type: ignore
            REQUEST_GROUP_NAME,
            {
                "type": "send.action",
                "code": army_person.code,
                "accepted": validated_data.action_response
            }
        )
        
    async def send_action(self, event: dict[str, str]):
        await self.send_json(event)