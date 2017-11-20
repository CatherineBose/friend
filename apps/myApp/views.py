from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from .models import *

# Create your views here.
# urlpatterns = [
#   url(r'^$', views.index),     # This line has changed!
#   url(r'^$', views.index),
#   url(r'^register$', views.register),
#   url(r'^login$', views.login),
#   url(r'^friends/$', views.friendsWall),
#   url(r'users/(?P<id>\d+)',views.show),
#   url(r'^logout$', views.logout)
# ]

def index(request):
    return render(request,'myApp/index.html')
    

def register(request):
    result = User.objects.register_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    print "result.id",result.id
    print request.session
    # if user_id  in request.session:
    print "result.id",result.id
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    usersFriends = User.objects.get(result.id).Friendships.all()
    print usersFriends
    context = {
        friendsList: usersFriends
    }
    return redirect('/friends', context)

def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect ('/')   
    request.session['user_id'] = result.id
    print "Successfully logged in!"
    messages.success(request, "Successfully logged in!")
    usersFriends = User.objects.get(result.id).Friendships.all()
    print usersFriends
    context = {
        friendsList: usersFriends
    }
    return redirect('/friends', context)
    # return redirect('/friends')

def wall(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')
    # request.session['count'] += 1
    context ={
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'myApp/friends.html', context)

def show(request, id):
    try:
        request.session['user_id']
    except KeyError:
        return redirect ('/')
    context ={
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'myApp/show.html')

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        print "Error while trying to logout"
    # return HttpResponse("You're logged out.")
    return redirect ('/')
