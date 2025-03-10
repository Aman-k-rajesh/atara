from django.urls import path
from . import views

urlpatterns = [
    # User-side chat URLs
    path("user_chat/", views.user_chat, name="user_chat"),
    path("user_chat/<int:service_id>/", views.user_chat, name="user_chat_with_service"),
    path("send_message/", views.send_message, name="send_message"),
    path("save_message/", views.save_message, name="save_message"),
    path("get_messages/", views.get_messages, name="get_messages"),
    path("get_services/", views.get_services, name="get_services"),
    path("chat/get_recent_chats/", views.get_recent_chats, name="get_recent_chats"),
    
    # Service-side chat URLs
    path("service_chat/", views.service_chat, name="service_chat"),
    path("get_service_messages/", views.get_service_messages, name="get_service_messages"),
    path("service_send_message/", views.service_send_message, name="service_send_message"),
    path("get_service_recent_chats/", views.get_service_recent_chats, name="get_service_recent_chats"),
    path("get_service_chat_users/", views.get_service_chat_users, name="get_service_chat_users"),
]