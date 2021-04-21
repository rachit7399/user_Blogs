from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
import uuid
from .UserManager import UserManager

class BaseModel(models.Model):
    """A base model to deal with all the asbtracrt level model creations"""

    # uuid field
    uid = models.UUIDField(default=uuid.uuid4,
                           primary_key=True,
                           editable=False)

    # date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(max_length=255, blank=False, default="demo_first_name")
    last_name = models.CharField(max_length=255, blank=False, default="demo_last_name")
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False)
    
    class Meta:
        db_table = "user"
        
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email   
        
    def tokens(self):
        return ''                
