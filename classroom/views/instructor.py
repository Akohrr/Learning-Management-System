from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from ..models import QuizOrAssignment, Question, Discussion, Comment
from .. import forms
from django.http import JsonResponse
# from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied



class TestInstructor(UserPassesTestMixin):
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            # Redirect the user to 403 page
            raise PermissionDenied
        if not self.request.user.groups.filter(name='Instructor Role').exists():
            # Redirect the user to 403 page
            raise PermissionDenied

        # Checks pass, let http method handlers process the request
        return self.dispatch

class ChoiceList(TestInstructor, ListView):

    def get_context_object_name(self, object_list):
        object_name = self.kwargs['choice']
        return object_name

    def get(self, request, *args, **kwargs):
        context = get_context_variables(self.kwargs['choice'], self.request.user)
        return self.render_to_response(context)

    def get_template_names(self):
        template = {
            'quizzes'    : r'classroom/instructor/quizzes.html',
            'assignments': r'classroom/instructor/assignments.html',
            'grades'     : r'classroom/instructor/grades.html',
            'discussions': r'classroom/instructor/discussions.html',
            }[self.kwargs['choice']]
        return [template]


class Choice(TestInstructor, CreateView):
    info = dict()

    def get_form(self, form_class=None):
        choice = self.kwargs['choice']
        form = {
            'assignment': forms.AssignmentForm,
            'quiz'      : forms.QuizForm,
            'comment'   : forms.CommentForm,
            'discussion': forms.DiscussionForm,
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


class QuestionAndCommentHandler(TestInstructor, CreateView):
    info = dict()

    def get_form(self, form_class=None):
        choice = self.kwargs['choice']
        form = {
            'quiz'      : forms.QuestionForm,
            'discussion' : forms.CommentForm,
        }[choice]
        return form(**self.get_form_kwargs())

    def get_form_kwargs(self):
        form_kwargs  = super(QuestionAndCommentHandler, self).get_form_kwargs()
        form_kwargs['user'] = self.request.user
        form_kwargs['pk'] = self.kwargs['pk']
        return form_kwargs

    def get(self, request, *args, **kwargs):
        path = request.META.get('PATH_INFO')
        choice = ('Comment' if kwargs['choice'] == 'discussion' else 'Question')

        form = self.get_form()
        context = {'path': path, 'form': form, 'choice':choice}
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)

    def form_valid(self, form):
        form.save()
        self.info['valid'] = True
        return JsonResponse(self.info)

    def form_invalid(self, form):
        path = self.request.META.get('PATH_INFO')
        choice = ('Comment' if self.kwargs['choice'] == 'discussion' else 'Question')
        context = {'path': path, 'form': form, 'choice': choice}
        self.info['valid'] = False
        self.info['html_form'] = render_to_string(
            'classroom/includes/new_form_modal.html', context)
        return JsonResponse(self.info)



def get_context_variables(choice, user=None):
    if user.user_type == 'IN':
        if choice == 'quizzes':
            quiz = QuizOrAssignment.objects.filter(is_assignment=False, owner=user).order_by('date_of_submission')[:21]
            questions = Question.objects.filter(quiz_or_assignment__owner=user)
            context = {'quizzes': quiz, 'questions':questions}
        elif choice == 'assignments':
            assignments = QuizOrAssignment.objects.filter(is_assignment=True, owner=user).order_by('date_of_submission')[:21]
            questions = Question.objects.filter(quiz_or_assignment__owner=user)
            context = {'assignments': assignments, 'questions':questions}
        elif choice == 'discussions':
            discussions = Discussion.objects.filter(course__instructors=user)
            comments = Comment.objects.filter(discussion__created_by=user)
            context = {'discussions':discussions, 'comments':comments}
            

        return context
    
    else:
        raise PermissionDenied