from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^$', views.index),     # This line has changed!
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^friends/$', views.wall),
  url(r'^user/(?P<id>\d+)',views.show),
  url(r'^logout$', views.logout),
    #   {{user.id}}/remove remove/{{user.id}}
  url(r'^remove/(?P<id>\d+)', views.logout),
  
]