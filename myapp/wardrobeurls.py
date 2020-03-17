from django.conf.urls import url, include
import myapp.wardrobeviews

urlpatterns = [
    url(r'getcloth', myapp.wardrobeviews.getcloth),
    url(r'newcloth', myapp.wardrobeviews.newcloth),
    url(r'delcloth', myapp.wardrobeviews.delcloth),
]