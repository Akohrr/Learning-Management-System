from django import forms
from accounts.models import User
from .models import Course, QuizOrAssignment, Question, Discussion, Comment
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group


class LMSAdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(
        help_text='Admin staff must use school(.lms) email address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def clean_email(self):
        if '.lms' not in self.cleaned_data['email']:
            raise forms.ValidationError(
                _('Invalid email address'), code='invalid')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'LA'
        lms_admins = Group.objects.get(name='Admin Role')
        if commit:
            user.save()
            user.groups.add(lms_admins)
        return user


class InstructorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(help_text='Please enter a valid email address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'IN'
        instructors = Group.objects.get(name='Instructor Role')
        if commit:
            user.save()
            user.groups.add(instructors)

        return user


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'ST'
        if commit:
            user.save()
        return user


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ('syllabus', 'modules',)

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['instructors'].queryset = User.objects.filter(
            user_type='IN').order_by('username')
        self.fields['students'].queryset = User.objects.filter(
            user_type='ST').order_by('username')
        self.fields['teaching_assistants'].queryset = User.objects.filter(
            user_type='TA').order_by('username')


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = QuizOrAssignment
        exclude = ('comment', 'owner', 'is_assignment',)

    def __init__(self, user, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        # declaring self.user so I can use (user) variable in save method
        self.user = user
        self.fields['course'].queryset = Course.objects.filter(
            instructors=user).order_by('instructors')

    def save(self, commit=True):
        assignment = super().save(commit=False)
        assignment.is_assignment = True
        assignment.owner = self.user
        if commit:
            assignment.save()
        return assignment


class QuizForm(forms.ModelForm):

    class Meta:
        model = QuizOrAssignment
        exclude = ('comment', 'owner', 'is_assignment',)

    def __init__(self, user, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        # declaring self.user so I can use (user) variable in save method
        self.user = user
        self.fields['course'].queryset = Course.objects.filter(
            instructors=user).order_by('instructors')

    def save(self, commit=True):
        quiz = super().save(commit=False)
        quiz.owner = self.user
        if commit:
            quiz.save()
        return quiz


class QuestionForm(forms.ModelForm):
    answer = forms.CharField(
        max_length=1, help_text='Enter the correct option (A or B or C or D)')

    class Meta:
        model = Question
        exclude = ('quiz',)

        widgets = {
            'first_option': forms.Textarea(attrs={'rows': '3'}),
            'second_option': forms.Textarea(attrs={'rows': '3'}),
            'third_option': forms.Textarea(attrs={'rows': '3'}),
            'fourth_option': forms.Textarea(attrs={'rows': '3'}),
        }

    def __init__(self, pk, user, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # declaring self.user and self.pk so I can use them in save method
        self.user = user
        self.pk = pk

    def clean_answer(self):
        data = self.cleaned_data
        correct_option = data['answer'].title()
        if correct_option not in ['A', 'B', 'C', 'D']:
            raise forms.ValidationError(
                _("Answer does not match any option"), code="no match")

        return correct_option

    def save(self, commit=True):
        quiz = QuizOrAssignment.objects.get(pk=self.pk)
        question = super().save(commit=False)
        question.quiz = quiz
        if commit:
            question.save()
        return question


class StudentQuestionForm(forms.ModelForm):
    answer = forms.CharField(max_length=1)

    class Meta:
        model = Question
        exclude = ('quiz_or_assignment', 'answer',)

        widgets = {
            'text': forms.Textarea(attrs={'readonly': 'readonly'}),
            'first_option': forms.Textarea(attrs={'readonly': 'readonly'}),
            'second_option': forms.Textarea(attrs={'readonly': 'readonly'}),
            'third_option': forms.Textarea(attrs={'readonly': 'readonly'}),
            'fourth_option': forms.Textarea(attrs={'readonly': 'readonly'}),
        }
    # def clean_sanswer(self):
    #     if self.cleaned_data['answer'].title() not in ['A', 'B', 'C', 'D']:
    #         raise forms.ValidationError(_('Answer does not match any option'), code="no match")


class BaseQuestionFormSet(forms.BaseModelFormSet):
    score = 0

    def clean(self):
        super().clean()

        for form in self.forms:
            try:
                if form.cleaned_data['answer'].title() not in ['A', 'B', 'C', 'D']:
                    raise forms.ValidationError(
                        _('One or more of your answer(s) does not match any option'), code='no match')
            except KeyError:
                raise forms.ValidationError(_('Please, answer all question before submitting'),code='invalid')

QuestionFormSet = forms.modelformset_factory(
    Question, form=StudentQuestionForm, extra=0, formset=BaseQuestionFormSet, can_delete=False)


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        exclude = ('created_by',)

    def __init__(self, user, *args, **kwargs):
        super(DiscussionForm, self).__init__(*args, **kwargs)
        # declaring self.user so I can use (user) variable in save method
        self.user = user
        self.fields['course'].queryset = Course.objects.filter(
            instructors=user)

    def save(self, commit=True):
        discussion = super().save(commit=False)
        discussion.created_by = self.user
        if commit:
            discussion.save()
        return discussion


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'discussion',)

    def __init__(self, pk, user, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        # declaring self.user and self.pk so I can use them in save method
        self.user = user
        self.pk = pk

    def save(self, commit=True):
        discussion = Discussion.objects.get(pk=self.pk)
        comment = super().save(commit=False)
        comment.author = self.user
        comment.discussion = discussion
        if commit:
            comment.save()
        return comment
