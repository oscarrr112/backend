from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import static
from django.conf import settings
import myapp.userurls
import myapp.wardrobeurls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'user/', include(myapp.userurls)),
    url(r'wardrobe/', include(myapp.wardrobeurls)),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
]