from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ops', 'Operation User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=False)

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    allowed_extensions = ['pptx', 'docx', 'xlsx']

    def save(self, *args, **kwargs):
        if self.file.name.split('.')[-1] not in self.allowed_extensions:
            raise ValueError("File type not allowed")
        super().save(*args, **kwargs)
