from django.conf.urls import url
from .views import lms_admin, instructor, student

urlpatterns = [

    url(r'^lms-admin/(?P<choice>[\w\-]+)/$',
        lms_admin.ChoiceList.as_view(), name='lms_admin_view'),

    url(r'^lms-admin/add/(?P<choice>[\w\-]+)/$',
        lms_admin.SignUpView.as_view(), name='lms_admin_add'),

    # url(r'^update/(?P<choice>[\w\-]+)/(?P<pk>\d+)/$',lms.),

    url(r'^instructor/(?P<choice>[\w\-]+)/$',
        instructor.ChoiceList.as_view(), name='instructor_view'),

    # url used to add a quiz or assignment
    url(r'^instructor/add/(?P<choice>[\w\-]+)/$',
        instructor.Choice.as_view(), name='instructor_add'),

    # url used to add questions to both quiz and assignment
    url(r'^instructor/add/(?P<choice>[\w\-]+)/(?P<pk>\d+)/$',
        instructor.QuestionAndCommentHandler.as_view(), name='instructor_add_choice'),

    url(r'^student/(?P<choice>[\w\-]+)/$',
        student.ChoiceList.as_view(), name='student_view'),

    url(r'^student/answer-question/(?P<pk>[\w\-]+)/$',
        student.take_questions, name='student_question'),





]
