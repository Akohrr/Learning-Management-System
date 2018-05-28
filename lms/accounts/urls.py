from django.conf.urls import url
from django.contrib.auth import views as authviews


urlpatterns = [
    url(r'^login/$', authviews.login, name='login'),
    url(r'^logout/$', authviews.logout, name='logout'),
    url(r'^logout-then-login/$', authviews.logout_then_login, name='logout_then_login'),
]