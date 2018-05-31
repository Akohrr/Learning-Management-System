from django.views.generic import ListView
from ..models import Course, QuizOrAssignment
# from datetime import datetime
from django.utils import timezone
from django.views.generic.edit import CreateView
from ..forms import QuestionFormSet
from django.http import JsonResponse
from django.template.loader import render_to_string
from classroom.models import Question


class ChoiceList(ListView):

    def get_context_object_name(self, object_list):
        object_name = self.kwargs['choice']
        return object_name

    def get(self, request, *args, **kwargs):
        context = get_context_variables(self.kwargs['choice'], self.request.user)
        return self.render_to_response(context)

    def get_template_names(self):
        template = {
            'courses'    : r'classroom/student/courses.html',
            'assignments': r'classroom/student/assignments.html',
            'quizzes'    : r'classroom/student/quizzes.html',
            'grades'     : r'classroom/student/grades.html',            
            'discussions': r'classroom/student/discussions.html',
            }[self.kwargs['choice']]
        return [template]



class TakeQuizOrAssignment(CreateView):
    info = dict()

    def get_form(self, form_class=None):
        code = self.kwargs['code']
        # form = {
        #     'assignment': forms.AssignmentForm,
        #     'quiz'      : forms.QuizForm,
        #     # 'grade'     : forms.GradeForm,
        #     # 'comment'   : forms.CommentForm,
        # }[choice]
        formset = QuestionFormSet(queryset=Question.objects.filter(quiz__course__code=code))
        return formset(**self.get_form_kwargs())


    # def get_form_kwargs(self):
    #     form_kwargs  = super(TakeQuizOrAssignment, self).get_form_kwargs()
    #     form_kwargs['user'] = self.request.user
    #     return form_kwargs

    def get(self, request, *args, **kwargs):
        path = request.META.get('PATH_INFO')
        form = self.get_form()
        context = {'path': path, 'form': form, 'choice': self.kwargs['choice']}
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)

    def form_valid(self, form):
        form.save()
        self.info['valid'] = True
        return JsonResponse(self.info)

    def form_invalid(self, form):
        path = self.request.META.get('PATH_INFO')
        context = {'path': path, 'form': form, 'choice': self.kwargs['choice']}
        self.info['valid'] = False
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)






def take_questions(request, code):
    """
    Extracts data of Souls from excel sheet and convert to Json object
    """
    info = dict()
    formset = QuestionFormSet(queryset=Question.objects.filter(quiz__course__code=code))
    path = request.META.get('PATH_INFO')
    # print(formset)
    # import time
    # time.sleep(6000)
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            print(formset)
            import time
            time.sleep(6000)
            info['saved_successfully'] = True
        else:
            info['saved_successfully'] = False
    context = {'formset':formset, 'is_formset':True, 'path':path}
    info['html_form'] = render_to_string('classroom/includes/new_form_modal.html', context)

    return JsonResponse(info)






def get_context_variables(choice, user=None):

    if user.user_type == 'ST':
        if choice == 'courses':
            courses = Course.objects.filter(students=user)
            context = {'courses':courses}
        elif choice == 'assignments':
            pending_assignments = QuizOrAssignment.objects.filter(date_of_submission__gt=timezone.now(), course__students=user, is_assignment=True)
            submitted_assignments = QuizOrAssignment.objects.filter(date_of_submission__lt=timezone.now(), course__students=user, is_assignment=True)
            context = {'pending_assignments': pending_assignments, 'submitted_assignments':submitted_assignments}
        elif choice == 'quizzes':
            pending_quizzes = QuizOrAssignment.objects.filter(date_of_submission__gt=timezone.now(), course__students=user, is_assignment=False)
            submitted_quizzes = QuizOrAssignment.objects.filter(date_of_submission__lt=timezone.now(), course__students=user, is_assignment=False)
            context = {'pending_quizzes': pending_quizzes, 'submitted_quizzes': submitted_quizzes}
        else:
            return -1

        return context

    else:
        return -1