# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     STATUS_CHOICES = (
#         ('user', 'user'),
#         ('etablissement', 'Etablissement'),
#     )
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)

#     def __str__(self):
#         return self.email
# models.py
# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class User(AbstractUser):
    STATUS_CHOICES = (
        ('client', 'Client'),
        ('etablissement', 'Etablissement'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. 150 characters or fewer.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] 
    def save(self, *args, **kwargs):
        if not self.username:
            # Générer un username unique à partir de l'email
            base_username = slugify(self.email.split('@')[0])
            counter = 1
            new_username = base_username
            while User.objects.filter(username=new_username).exists():
                new_username = f"{base_username}{counter}"
                counter += 1
            self.username = new_username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
