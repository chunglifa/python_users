from django.conf.urls import url
from . import views


urlpatterns = [
# LOGIN REGISTRATION
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),

#  OTHER PAGES
    url(r'^welcome/$', views.welcome),
    url(r'^users/(?P<id>\d+)$', views.user),
    url(r'^myaccount/(?P<id>\d+)$', views.edit),

# PROCESSING METHODS
    url(r'^add_quote$', views.add_quote),
    url(r'^like$', views.like),
    url(r'^update$', views.update),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]