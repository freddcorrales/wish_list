from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User
from datetime import datetime

class ListManager(models.Manager):
    def valid(self, postData):
        response = {
            'valid':  True,
            'errors': [],
        }
        if len(postData['item']) < 1:
            response['errors'].append('Item cannot be blank')
        if len(postData['item']) < 3:
            response['errors'].append('Item name must be at least 3 characters')

        if len(response['errors']) > 0:
            response['valid'] = False

        return response

class List(models.Model):
    item = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    users = models.ManyToManyField(User, related_name = 'user_items')
    objects = ListManager()
    
