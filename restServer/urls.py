from django.conf.urls import include, url
from restServer.views import *

urlpatterns = [
    
    url(r'^$', registerView.as_view() , name = 'register'),
    url(r'^post/$', postView.as_view() , name = 'userPost'),
    url(r'^success/(?P<code>[a-zA-Z0-9!@#$&()\\ -`.+,/\"]*)/$', successView.as_view() , name = 'success'),
    url(r'^error/(?P<code>[a-zA-Z0-9!@#$&()\\ -`.+,/\"]*)/$', errorView.as_view() , name = 'error'),
    url(r'^verify/(?P<code>[a-zA-Z0-9!@#$&()\\ -`.+,/\"]*)/$', verifyView.as_view() , name = 'verify'),
]
