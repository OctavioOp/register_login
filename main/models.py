from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.urls.resolvers import URLPattern
import re

# Create your models here.


class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        NUM_REGEX = re.compile('[0-9]')
        if len(postData['name']) < 2:
            errors['name'] = 'name needs more than 3 letters'
        if NUM_REGEX.match(postData['name']):
            errors['name'] = 'only letters are allowed'
        if len(postData['password']) < 8:
            errors['password'] = 'Password has 8 characters'
        if postData['password'] != postData['password_confirm']:
            errors['password']= "Passwords doesn't match"
        return errors


class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()
