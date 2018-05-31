

from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView
from .. import forms
from django.template.loader import render_to_string
# from django.conf import settings.AUTH_USER_MODEL as User
from accounts.models import User
from django.http import JsonResponse, Http404
from django.contrib.auth.models import Group
from django.views.generic.edit import FormMixin
from .. models import Course


class ChoiceList(ListView):

    def get_context_object_name(self, object_list):
        object_name = self.kwargs['choice']
        return object_name

    def get_queryset(self):
        choice = self.kwargs['choice']
        try:
            if len(choice) == 2:
                user_type = {
                    'lms-admins' : 'LA',
                    'instructors': 'IN',
                    'students'   : 'ST',
                    }
                queryset = User.objects.filter(user_type=user_type[choice])
            elif choice == 'courses':
                queryset = Course.objects.all()
            else:
                raise Http404 
        except:
            raise Http404
        return queryset

    def get_template_names(self):
        template = {
            'lms-admins' : r'classroom/lms_admin/lms_admins.html',
            'instructors': r'classroom/lms_admin/instructors.html',
            'students'   : r'classroom/lms_admin/students.html',
            'courses'    : r'classroom/lms_admin/courses.html',
            }[self.kwargs['choice']]
        return [template]





# view used to handle creation of lms_admin, instructors, students, courses
class SignUpView(CreateView):
    info = dict()
    model = User

    def get_form(self, form_class=None):
        choice = self.kwargs['choice']
        form = {
            'lms_admin' : forms.LMSAdminSignUpForm,
            'instructor': forms.InstructorSignUpForm,
            'student'   : forms.StudentSignUpForm,
            'course'    : forms.CourseForm,
        }[choice]
        return form(**self.get_form_kwargs())


    def get(self, request, *args, **kwargs):
        choice = self.kwargs['choice']
        form = self.get_form()
        context = {'form': form, 'choice': choice.title()}
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)

    def form_valid(self, form):
        form.save()
        self.info['valid'] = True
        return JsonResponse(self.info)

    def form_invalid(self, form):
        context = {'form': form, 'choice': 'Instructor'}
        self.info['valid'] = False
        self.info['html_form'] = render_to_string(
            'classroom/includes/modal.html', context)
        return JsonResponse(self.info)

