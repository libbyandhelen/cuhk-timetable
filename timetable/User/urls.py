from django.conf.urls import url

from User.views import create_user, user_login, user_logout

urlpatterns = [
    url(r'^$', create_user),
    url(r'^login$', user_login),
    url(r'^logout$', user_logout),
]
