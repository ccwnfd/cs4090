from django.db import models
from accounts.models.user import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    url = models.URLField()
    icon = models.CharField(max_length=50)
    icon_color = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
