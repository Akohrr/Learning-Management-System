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

    def get_template_names(self):
        template = {
            'quiz'       : r'classroom/instructor/quiz.html',
            'assignments': r'classroom/instructor/assignments.html',
            'grades'     : r'classroom/instructor/grades.html',
            }[self.kwargs['choice']]
        return [template]







class Choice(CreateView):
    info = dict()

    def get_form(self, form_class=None):
        choice = self.kwargs['choice']

        form = {
            'assignment': forms.AssignmentForm,
            'quiz'      : forms.QuizForm,
            # 'grade'     : forms.GradeForm,
            # 'comment'   : forms.CommentForm,
        }[choice]
        return form(**self.get_form_kwargs())

    def get_form_kwargs(self):
        form_kwargs  = super(Choice, self).get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

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


class QuestionHandler(CreateView):
    info = dict()
    form_class = forms.QuestionForm

    def get_form_kwargs(self):
        form_kwargs  = super(QuestionHandler, self).get_form_kwargs()
        form_kwargs['user'] = self.request.user
        form_kwargs['pk'] = self.kwargs['pk']
        return form_kwargs

    def get(self, request, *args, **kwargs):
        path = request.META.get('PATH_INFO')
        form = self.get_form()
        context = {'path': path, 'form': form, 'choice': 'Question'}
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)

    def form_valid(self, form):
        form.save()
        self.info['valid'] = True
        return JsonResponse(self.info)

    def form_invalid(self, form):
        path = self.request.META.get('PATH_INFO')
        context = {'path': path, 'form': form, 'choice': 'Question'}
        self.info['valid'] = False
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)



def get_context_variables(choice, user=None):
    if choice == 'quiz':
        quiz = Quiz.objects.filter(is_assignment=False, owner=user).order_by('date_of_submission')[:21]
        questions = Question.objects.filter(quiz__owner=user)
        context = {'quizes': quiz, 'questions':questions}
    elif choice == 'assignments':
        assignments = Quiz.objects.filter(is_assignment=True, owner=user).order_by('date_of_submission')[:21]
        questions = Question.objects.filter(quiz__owner=user)
        context = {'assignments': assignments, 'questions':questions}


    return context