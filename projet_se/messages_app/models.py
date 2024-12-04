from django.db import models
from django.conf import settings  # Import pour utiliser AUTH_USER_MODEL

class Message(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    unread_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.created_at}"
