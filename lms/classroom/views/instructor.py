from django.shortcuts import render
from django.views.generic import CreateView
from ..models import Quiz
from .. import forms
from django.http import JsonResponse
from django.template.loader import render_to_string



def home(request):
    return render(request, r'classroom/instructor/quiz.html')


class Assignmentt(CreateView):
    info = dict()
    model = Quiz

    def get_form(self, form_class=None):
        # choice = self.kwargs['choice']
        # form = {
        #     'lms_admin' : forms.LMSAdminSignUpForm,
        #     'instructor': forms.InstructorSignUpForm,
        #     'student'   : forms.StudentSignUpForm,
        #     'course'    : forms.AddCourseForm,
        # }[choice]
        form = forms.AddAssignmentForm(user=self.request.user)
        return form(**self.get_form_kwargs())


    def get(self, request, *args, **kwargs):
        # choice = self.kwargs['choice']
        form = self.get_form()
        context = {'form': form}
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