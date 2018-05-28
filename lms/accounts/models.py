from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

# Create your models here.
class User(AbstractUser):
    USER_ROLE = (
        ('AD', 'System Admin'),
        ('LA', 'Admin'),
        ('IN', 'Instructor'),
        ('TA', 'Teaching Assistant'),
        ('ST', 'Student'),
    )

    user_type = models.CharField(max_length=2, choices=USER_ROLE)

    # def get_absolute_url(self):
    #     return reverse('classroom:update_user', kwargs={'user_type':self.user_type, 'pk':str(self.pk)})
