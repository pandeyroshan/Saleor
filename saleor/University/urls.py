from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"",
        views.home,
        name="home",
    ),
]


'''
There can be several URLPatterns here, each corresponding to unique functions in views.py

'''