from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def register(self, name, username, password, confirm, date_hired):
        response = {
            'valid': True,
            'errors': [],
            'user': None
        }

        if len(name) < 1:
            response['errors'].append('First name is required')
        elif len(name) < 2:
            response['errors'].append('First name must be 2 characters or longer')

        if len(username) < 1:
            response['errors'].append('Username is required')
        elif len(username) < 3:
            response['errors'].append('Username must be 3 characters or longer')
        else:
            #get only returns 1 thing, filter gets a list, if more than one thing, then get and NOT filter will break
            username_list = User.objects.filter(username = username.lower()) 
            if len(username_list) > 0:
                response['errors'].append('Username already in use')               

        # DELETE BUT USE THE SAME LOGIC FOR TRAVEL START AND TRAVEL END
        # if len(dob) < 1:
        #     response['errors'].append('Date of birth is required')
        # else:
        #     # comes back as a string (stringParseTime) in unicode YOU MUST GO TO TERMINAL TO SEE IF IT"S COMING BACK CORRECTLY AND MATCH THAT FORMAT
        #     date = datetime.strptime(dob, '%Y-%m-%d') 
        #     today = datetime.now()
        #     if date > today:
        #         response['errors'].append('Date of birth must be in the past')

        if len(password) < 1:
            response['errors'].append('Password is required')
        elif len(password) < 8:
            response['errors'].append('Password must be 8 characters or longer')   

        if len(confirm) < 1:
            response['errors'].append('Confirm password is required')
        elif confirm != password:
            response['errors'].append('Confirm password must match password')
        
        if len(date_hired) < 1:
            response['errors'].append('Missing Date Hired')
        
        if len(response['errors']) > 0:
            response['valid'] = False
        else:
            #created a record in your database, check SQLlite
            response['user'] = User.objects.create( 
                name = name,
                username = username,
                #hash your password
                password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                date_hired = datetime.strptime(date_hired, "%Y-%m-%d") 
            )
        # the above response will be sent back to the views.py
        return response 
            
    
    def login(self, username, password):
        response = {
            'valid': True,
            'errors': [],
            'user': None
        }

        if len(username) < 1:
            response['errors'].append('Username is required')
        else:
            #get only returns 1 thing, filter gets a list, if more than one thing, then get and NOT filter will break
            username_list = User.objects.filter(username = username)
            if len(username_list) == 0:
                response['errors'].append('Unknown Username')   

        if len(password) < 1:
            response['errors'].append('Password is required')
        elif len(password) < 8:
            response['errors'].append('Password must be 8 characters or longer')   

        if len(response['errors']) == 0:
            hashed_pw = username_list[0].password
            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                #remember, we generated username_list up above and now the list contains information about that specific user that we are returning
                response['user'] = username_list[0] 
            else:
                response['errors'].append('Incorrect Password')
        
        if len(response['errors']) > 0:
            response['valid'] = False
        return response

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    # def __repr__(self):
    #     return '{} | {} '.format(self.first_name, self.last_name)


