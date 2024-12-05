import json
from channels.generic.websocket import WebsocketConsumer
from EmailCompositionAndManagement.models import *
from asgiref.sync import async_to_sync
from landing.models import CustomUser
from .models import Notification
import traceback

class AppNotifications(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]

        # Change the group name to 'global_notif' for global notifications
        self.room_group_name = "global_notif"

        # Add the user to the 'global_notif' group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Remove user from the 'global_notif' group when disconnected
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):
        email_data = text_data['email']

        from_user_id = email_data.get('fromUser')
        to_user_id = email_data.get('toUser')
        subject = email_data.get('subject')
        content = email_data.get('content')

        try:
            from_user = CustomUser.objects.filter(id=from_user_id).first()
            to_user = CustomUser.objects.filter(username=to_user_id).first()

            email = Email.objects.get_or_create(
                fromUser = from_user,
                toUser = to_user,
                subject = email_data["subject"],
                content = email_data["content"]
            )



            # Send the notification to the 'global_notif' group (broadcast to all users)
            # async_to_sync(self.channel_layer.group_send)(
            #     'global_notif',  # Using the 'global_notif' group name for global notifications
                # {
                #     'type': 'email_notification',
                #     'email': {
                #         'toUser': to_user.username,
                #         'fromUser': from_user.username,
                #         'subject': subject,
                #         'content': content,
                #         'emailId' : email[0].id,
                #         'fromUserId' : from_user_id,
                #         'is_read' : False
                #     }
                # }
            # )

            self.send(text_data=json.dumps(
                {
                    'type': 'email_notification',
                    'email': {
                        'toUser': to_user.username,
                        'fromUser': from_user.username,
                        'subject': subject,
                        'content': content,
                        'emailId' : email[0].id,
                        'fromUserId' : from_user_id,
                        'is_read' : False
                    }
                }))
        except CustomUser.DoesNotExist:
            self.send(text_data=json.dumps({
                'result': 'Invalid User(s) specified'
            }))
        except Exception as e:
            self.send(text_data=json.dumps({
                'result': f'Error: {e}'
            }))
