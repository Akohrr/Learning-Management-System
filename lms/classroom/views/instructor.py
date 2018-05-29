from django.shortcuts import render
from django.views.generic import CreateView, ListView
from ..models import Quiz, Question
from .. import forms
from django.http import JsonResponse
from django.template.loader import render_to_string



def home(request):
    return render(request, r'classroom/instructor/quiz.html')


class ChoiceList(ListView):

    def get_context_object_name(self, object_list):
        object_name = self.kwargs['choice']
        return object_name

    def get(self, request, *args, **kwargs):
        context = get_context_variables(self.kwargs['choice'], self.request.user)
        return self.render_to_response(context)
        # return render(self.request, 'classroom/instructor/quiz.html', context)

    def get_template_names(self):
        template = {
            'quiz' : r'classroom/instructor/quiz.html',
            'instructors': r'classroom/instructor/instructors.html',
            'students'   : r'classroom/instructor/students.html',
            'courses'    : r'classroom/instructor/courses.html',
            }[self.kwargs['choice']]
        return [template]







class Choice(CreateView):
    info = dict()
    # model = Quiz

    def get_form(self, form_class=None):
        choice = self.kwargs['choice']
        print(choice)
        # import time
        # time.sleep(600)
        form = {
            # 'assignment'      : forms.QuizForm,
            'quiz'      : forms.AssignmentForm,
            'question'  : forms.QuestionForm,
            # 'grade'     : forms.GradeForm,
            # 'comment'   : forms.CommentForm,
        }[choice]
        # form = forms.AddAssignmentForm
        return form(**self.get_form_kwargs())

    def get_form_kwargs(self):
        form_kwargs  = super(Choice, self).get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = {'form': form, 'choice': 'Quiz'}
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)

    def form_valid(self, form):
        form.save()
        # if self.
        # self.request.POST
        self.info['valid'] = True
        return JsonResponse(self.info)

    def form_invalid(self, form):
        context = {'form': form, 'choice': 'Quiz'}
        self.info['valid'] = False
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)



def get_context_variables(choice, user=None):
    if choice == 'quiz':
        quiz = Quiz.objects.filter(owner=user).order_by('date_of_submission')[:21]
        questions = Question.objects.filter(quiz__owner=user)#.order_by('date_of_submission')[:21]
        # print(questions)
        # import time
        # time.sleep(600)
        context = {'quizes': quiz, 'questions':questions}
        print(context)
        return context