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
from django.contrib.auth.mixins import UserPassesTestMixin


class TestStudent(UserPassesTestMixin):

    def test_func(self):
        if not self.request.user.is_authenticated:
            # Redirect the user to 403 page
            raise PermissionDenied
        if not self.request.user.user_type == 'ST':
            # Redirect the user to 403 page
            raise PermissionDenied

        # Checks pass, let http method handlers process the request
        return self.dispatch


class ChoiceList(TestStudent, ListView):
    """class-based view to list courses, assignments, quizzes and grades

    Arguments:
        TestStudent {class} -- Custom Mixin to prevent unauthorized users
        ListView {class} -- Django generic List View

    Raises:
        PermissionDenied -- exception thrown to prevent unauthorized access to this view
        PermissionDenied -- exception thrown to prevent unauthorized access to this view

    """
    def get_context_object_name(self, object_list):
        object_name = self.kwargs['choice']
        return object_name

    def get(self, request, *args, **kwargs):
        context = get_context_variables(
            self.kwargs['choice'], self.request.user)
        return self.render_to_response(context)

    def get_template_names(self):
        template = {
            'courses': r'classroom/student/courses.html',
            'assignments': r'classroom/student/assignments.html',
            'quizzes': r'classroom/student/quizzes.html',
            'grades': r'classroom/student/grades.html',
            'discussions': r'classroom/student/discussions.html',
        }[self.kwargs['choice']]
        return [template]


def take_questions(request, pk):
    """
    Returns questions as a formset to be answered by student
    """
    info = dict()
    questions = Question.objects.filter(quiz_or_assignment__id=pk)
    formset = QuestionFormSet(queryset=questions)
    date_of_submission = str(
        questions[0].quiz_or_assignment.date_of_submission)
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
            status = grade(request.user, score, pk)
            if status:
                info['submitted_successfully'] = True

            else:
                info['already_submitted'] = True

            return JsonResponse(info)
        else:
            info['submitted_successfully'] = False

    context = {'formset': formset, 'is_formset': True,
               'path': path, 'date_of_submission': date_of_submission}
    info['html_form'] = render_to_string(
        'classroom/includes/answer_question_modal.html', context)

    return JsonResponse(info)


def get_context_variables(choice, user):
    """To get the appropriate context variables based on the section 
        of the site a student wants to view

    Arguments:
        choice {string} -- section of the site to be viewed by a student. 
                            Possible options are course, quiz, assignment

    Keyword Arguments:
        user {object} -- user instance to cross-check that a that the user is a student

    Raises:
        PermissionDenied -- Prevents unauthorized users from viewing a students page
        PermissionDenied -- Prevents unauthorized users from viewing a students page

    Returns:
        [dictionary] -- appropriate context variables
    """

    if user.user_type == 'ST':
        if choice == 'courses':
            courses = Course.objects.filter(students=user)
            context = {'courses': courses}
        elif choice == 'assignments':
            pending_assignments = QuizOrAssignment.objects.filter(
                date_of_submission__gt=timezone.now(), course__students=user, is_assignment=True)
            submitted_assignments = QuizOrAssignment.objects.filter(
                date_of_submission__lt=timezone.now(), course__students=user, is_assignment=True)
            context = {'pending_assignments': pending_assignments,
                       'submitted_assignments': submitted_assignments}
        elif choice == 'quizzes':
            pending_quizzes = QuizOrAssignment.objects.filter(
                date_of_submission__gt=timezone.now(), course__students=user, is_assignment=False)
            submitted_quizzes = QuizOrAssignment.objects.filter(
                date_of_submission__lt=timezone.now(), course__students=user, is_assignment=False)
            context = {'pending_quizzes': pending_quizzes,
                       'submitted_quizzes': submitted_quizzes}
        elif choice == 'discussions':
            discussions = Discussion.objects.filter(course__students=user)
            comments = Comment.objects.filter(
                discussion__course__students=user)
            context = {'discussions': discussions, 'comments': comments}
        elif choice == 'grades':
            grades = Grade.objects.filter(student=user)
            context = {'grades': grades}
        else:
            raise PermissionDenied

        return context

    else:
        raise PermissionDenied


def grade(user, score, pk):
    """used to grade students based on their score in an assignment or quiz
    
    Arguments:
        user {object} -- user that is taking the assignment or quiz
        score {double} -- the number of questions answered correctly 
                        divided by total number of questions

        pk {int} -- primary key of the quiz or assignment

        NOTE: multiple questions belong to a quiz or assignment
    
    Returns:
        status {bool} -- The fuction checks to make sure the student has no been 
        graded in that particular quiz or assignment
        True == No grade before
    """
    quiz_or_assignment = QuizOrAssignment.objects.get(pk=pk)
    code = quiz_or_assignment.course.code
    # check if a grade exists for a student in that particular course
    if Grade.objects.filter(quiz_or_assignment=quiz_or_assignment, student=user, course__code=code).exists():
        return False
    else:
        # if grade does not exist create a new grade for the student in the particular course
        course = Course.objects.get(code=code)
        Grade.objects.create(quiz_or_assignment=quiz_or_assignment,
                             student=user, course=course, score=score)
        return True
