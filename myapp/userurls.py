from django.conf.urls import url, include
import myapp.userviews

urlpatterns = [
    url(r'register', myapp.userviews.register),
    url(r'login', myapp.userviews.login),
    url(r'findpassword1', myapp.userviews.findpassword1),
    url(r'findpassword2', myapp.userviews.findpassword2),
    url(r'getinfo', myapp.userviews.getinfo),
    url(r'editinfo', myapp.userviews.editinfo),
    url(r'addmodel', myapp.userviews.addmodel),
    url(r'getmodel', myapp.userviews.getmodel)
]