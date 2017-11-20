from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
import datetime
from time import gmtime, strftime

emailFilterREGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameFilterREGEX = re.compile(r'^[^\W_]+(-[^\W_]+)?$', re.U)

# Create your models here.
class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = []
        if len(self.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])[0]
            # check this user's password
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('password incorrect, check if caps lock is on')
        else:
            errors.append('email incorrect')
        if errors:
            return errors
        return user

    def register_validator(self,postData):
        #Initialize empty array for errors 
        errors = [] 
        # check first name and last name length
        name = str(postData['name'])
        alias= str(postData['alias'])
        if len(name) < 2: 
            errors.append("User name and alias should be more than 2 characters")
        if len(alias) < 2:
            errors.append("alias should be more than 2 characters")
        # check password
        if len(postData['password']) < 8:
            errors.append("Password should have more than 8 characters") 
        # check first_name and last_name for valid characters
        # if not re.match(nameFilterREGEX, postData['name']) or not re.match(nameFilterREGEX, postData['alias']):
        #     errors.append("User name and alias should contains only letters no special characters allowed") 
        # 
        name = postData['name']
        print "type(name)", type(name)
        print name
        nameString = str (name)
        print "nameString: ", nameString
        print "nameString.isalpha(): ", nameString.isalpha()
        # if not nameString.isalpha():
        if not all(i.isalpha() or i==' ' for i in nameString):
            errors.append("User name should contains only letters no special characters allowed ")
        #Alias
        alias = postData['alias']
        aliasString = str (alias)
        # if not str(postData['alias']).isalpha():
        if not all(i.isalpha() or i==' ' for i in aliasString):
            # print "str(postData['alias'])", str(postData['alias'])
            # print "str(postData['alias']).isalpha(): ", str(postData['alias']).isalpha()
            errors.append("alias should contains only letters no special characters allowed")
        # check email with Email_REgex
        if not re.match(emailFilterREGEX, postData['email']):
            errors.append("Not a valid email")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("email already in use") 
        # check password
        if postData['password'] != postData['confirm']:
            errors.append("Password doesn't match")
        # # check if password has one capital letter and one no
        passWdString = postData['password']
        print "passWdString: ", passWdString
        if not (any(x.isupper() for x in passWdString) ):
            print passWdString + " passWdString is not a valid password"
            errors.append("Password should have at least one capital letter ")
        # check if password has one no
        if not(any(x.isdigit() for x in passWdString)):
            errors.append("Password should have at least one digit")
        current_date = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        print "current_date",current_date
        user_bday = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
        print "user_bday", user_bday
        try:
            if user_bday > current_date:
                    errors.append ("Enter the date that you were born not future date")
        except:
            errors.append ("Please input a birth date")
        # try:
        #     # current_date = datetime.now().date()
        #     current_date = datetime.datetime.strptime(str(datetime.date.today()),'%Y-%m-%d')
        #     print current_date
        #     user_bday = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
        #     print user_bday
        #     if user_bday > current_date:
        #         errors.append ("Enter the date that you were born not future date")
        # except:
        #     errors.append ("Please input a birth date")
        print "errors List \n", errors
        print "name=postData['name']", postData['name']
        print "alias=postData['alias']", postData['alias']
        print "email=postData['email']", postData['email']
        print "password", postData['password']
        print "birthday = postData['birthday']", postData['birthday']
        
       
        if not errors:
                print "Inside hash password"
                # add a new user
                # hash password
                hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
                print "hashed code: ", hashed
                new_user = self.create(
                    name=postData['name'],
                    alias=postData['alias'],
                    email=postData['email'],
                    password=hashed,
                    birthday = postData['birthday']
                )
                return new_user
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.TextField(max_length=45)
    password = models.CharField(max_length=45)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Friendships = models.ManyToManyField('self')
    objects = UserManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.id, self.name, self.email, self.birthday)

'''
from apps.myApp.models import *
user1 = User.objects.get(id =1)
user2 = User.objects.get(id =2)
user3 = User.objects.get(id =3)
user4 = User.objects.get(id =4)
User.objects.get(id=1).Friendships.add(User.objects.get(id=2))
User.objects.get(id=1).Friendships.add(User.objects.get(id=2))
User.objects.get(id=1).Friendships.add(User.objects.get(id=3))
User.objects.get(id=2).Friendships.add(User.objects.get(id=3))
User.objects.get(id=2).Friendships.add(User.objects.get(id=4))
User.objects.get(id=2).Friendships.all()

'''
