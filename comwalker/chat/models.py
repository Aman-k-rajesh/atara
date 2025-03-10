from django.db import models

# Create your models here.
from django.utils.timezone import now
from django.db import models
from user.models import com_TB  # Import User model
from service.models import Service_DB  # Import Service model

class Messages_Tb(models.Model):
    sender_user = models.ForeignKey(com_TB, on_delete=models.CASCADE, null=True, blank=True, related_name="sent_messages")
    sender_service = models.ForeignKey(Service_DB, on_delete=models.CASCADE, null=True, blank=True, related_name="sent_messages_service")
    receiver_user = models.ForeignKey(com_TB, on_delete=models.CASCADE, null=True, blank=True, related_name="received_messages")
    receiver_service = models.ForeignKey(Service_DB, on_delete=models.CASCADE, null=True, blank=True, related_name="received_messages_service")
    
    message = models.TextField(default="No message") 
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Track if the message has been read

    def __str__(self):
        return f"From {self.get_sender()} to {self.get_receiver()}"

    def get_sender(self):
        """Returns sender's name whether it's a user or a service"""
        return self.sender_user.FullName if self.sender_user else self.sender_service.CentreName

    def get_receiver(self):
        """Returns receiver's name whether it's a user or a service"""
        return self.receiver_user.FullName if self.receiver_user else self.receiver_service.CentreName