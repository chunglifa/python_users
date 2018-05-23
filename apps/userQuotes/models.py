from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from bcrypt import checkpw


class UserManager(models.Manager):
    def registration_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "FIRST NAME MUST BE LONGER THAN 2"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "LAST NAME MUST BE LONGER THAN 2"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email not in correct format"
        if User.objects.filter(email = postData['email']):
            errors['email'] = "EMAIL ALREADY EXISTS"
        if len(postData['password']) < 8:
            errors["password"] = "PASSWORD MUST BE LONGER THAN 8 CHARACTERS"
        if postData['password'] != postData['password_check']:
            errors["password_check"] = "PASSWORD DON'T MATCH"
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])) < 1: 
            errors['email'] = 'Email does not exist'
        else:
            print('\nEMAIL MATCHES, CHECKING PASSWORD\n')
            user = User.objects.filter(email = postData['email'])
            if len(postData['password']) <1:
                errors['password'] = 'Password is less than 1 character?!'
            elif not checkpw(postData['password'].encode(), user[0].pw_hash.encode()):
                errors['password'] = 'PASSWORDS DO NOT MATCH'
                print('passwords match')
        return errors
    def update_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "FIRST NAME MUST BE LONGER THAN 2"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "LAST NAME MUST BE LONGER THAN 2"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email not in correct format"
        if User.objects.filter(email = postData['email']):
            errors['email'] = "EMAIL ALREADY EXISTS"
        return errors

class QuoteManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['quote']) < 10:
            errors["quote"] = "QUOTE MUST EXIST"
        if len(postData['author']) < 3:
            errors["author"] = "AUTHOR MUST BE GREATER THAN 3"
        return errors

class LikeManager(models.Manager):
    def review_validator(self, postData):
        errors = {}
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash =  models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name = "uploaded_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    objects = QuoteManager()

class Like(models.Model):
    user = models.ForeignKey(User, related_name = 'likes')
    quote = models.ForeignKey(Quote, related_name = 'likes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = LikeManager()

