# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from notifications_app.models import AccountChangeNotification, EmailNotification

# def handle_account_change(user, change_type, details=None):
#     notification = AccountChangeNotification.objects.create(
#         user=user,
#         change_type=change_type,
#         details=details
#     )
#     notify_via_websocket(user, notification)

# def handle_email_notification(user, from_user, subject):
#     notification = EmailNotification.objects.create(
#         user=user,
#         from_user=from_user,
#         subject=subject
#     )
#     notify_via_websocket(user, notification)

# def notify_via_websocket(user, notification):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"user_{user.id}",
#         {
#             "type": "send_notification",
#             "message": {
#                 "type": notification.__class__.__name__,
#                 "data": {
#                     "id": notification.id,
#                     "timestamp": str(notification.timestamp),
#                     **(notification.__dict__)
#                 },
#             }
#         }
#     )
