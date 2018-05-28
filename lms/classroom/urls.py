from django.conf.urls import url
from .views import lms_admin, instructor

urlpatterns = [
    
    url(r'^lms-admin/(?P<choice>[\w\-]+)/$', lms_admin.UserList.as_view()),
    url(r'^lms-admin/add/(?P<choice>[\w\-]+)/$', lms_admin.SignUpView.as_view(), name='add_user'),
    # url(r'^update/(?P<choice>[\w\-]+)/(?P<pk>\d+)/$',lms.),
    url(r'^instructor/$', instructor.home),
    url(r'^instructor/add/(?P<choice>[\w\-]+)/$', instructor.Assignmentt.as_view()),
    

]