from django.views.generic import ListView
from ..models import Course, QuizOrAssignment
# from datetime import datetime
from django.utils import timezone
from django.views.generic.edit import CreateView
from ..forms import QuestionFormSet
from django.http import JsonResponse
from django.template.loader import render_to_string
from classroom.models import Question, Grade, QuizOrAssignment, Discussion, Comment
from django.core.exceptions import PermissionDenied


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


def take_questions(request, pk):
    """
    Returns question as a formset
    """
    info = dict()
    questions = Question.objects.filter(quiz_or_assignment__id=pk)
    formset = QuestionFormSet(queryset=questions)
    time_left_till_submission = timezone.now() - questions[0].quiz_or_assignment.date_of_submission
    print(time_left_till_submission.seconds)
    import time
    time.sleep(6000)
    path = request.META.get('PATH_INFO')
    score = 0

    if request.method == 'POST':
        formset = QuestionFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                student_option = form.cleaned_data['answer'].title()
                correct_option = form.instance.answer
                if student_option == correct_option:
                    score += 1
            score = (score/len(formset)) * 100
            print(score)
            status = grade(request.user, score, pk)
            print(status)
            if status:
                info['submitted_successfully'] = True
                
            else:
                info['already_submitted'] = True
            
            return JsonResponse(info)
        else:
            info['submitted_successfully'] = False
            
    context = {'formset':formset, 'is_formset':True, 'path':path}
    info['html_form'] = render_to_string('classroom/includes/answer_question_modal.html', context)

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
        elif choice == 'discussions':
            discussions = Discussion.objects.filter(course__students=user)
            comments = Comment.objects.filter(discussion__course__students=user)
            context = {'discussions':discussions, 'comments':comments}
        elif choice == 'grades':
            grades = Grade.objects.filter(student=user)
            context={'grades':grades}
        else:
            raise PermissionDenied

        return context

    else:
        raise PermissionDenied


def  grade(user, score, pk):
    quiz_or_assignment = QuizOrAssignment.objects.get(pk=pk)
    code = quiz_or_assignment.course.code
    #check if a grade exists for a student in that particular course
    if Grade.objects.filter(student=user, course__code=code).exists():
        return False
    else:
        #if grade does not exist create a new grade for the student in the particular course
        course = Course.objects.get(code=code)
        Grade.objects.create(quiz_or_assignment=quiz_or_assignment, student=user, course=course, score=score)
        return True