from django import forms
from accounts.models import User 
from .models import Course, Quiz, Question
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import 
from django.utils.translation import ugettext_lazy as _
# from ajax_select.fields import AutoCompleteSelectMultipleField
# import select2
# from select2.forms import Select2Widget


class LMSAdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(help_text='Admin staff must use school(.lms) email address')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def clean_email(self):
        if '.lms' not in self.cleaned_data['email']:
            raise forms.ValidationError(_('Invalid email address'), code='invalid')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'LA'
        if commit:
            user.save()
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
        if commit:
            user.save()
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
        self.fields['instructors'].queryset = User.objects.filter(user_type='IN')
        self.fields['students'].queryset = User.objects.filter(user_type='ST')
        self.fields['teaching_assistants'].queryset = User.objects.filter(user_type='TA')


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Quiz
        exclude = ('comment', 'owner', 'is_assignment',)

    def __init__(self, user, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        #declaring self.user so I can use (user) variable in save method
        self.user = user
        self.fields['course'].queryset = Course.objects.filter(instructors=user)
    
    def save(self, commit=True):
        assignment = super().save(commit=False)
        assignment.is_assignment = True
        assignment.owner = self.user
        if commit:
            assignment.save()
        return assignment 


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ()

    def clean_answer(self):
        data = self.cleaned_data
        for option in [data['first_option'], data['second_option'], data['third_option'], data['fourth_option']]:
            if option == data['answer']:
                return data['answer']

        raise forms.ValidationError(_("Answer does not match any option"), code="no match")

    
    # def save(self, commit=True):
        # assignment = super().save(commit=False)
        # assignment.is_assignment = True
        # assignment.owner = self.user
        # if commit:
        #     assignment.save()
        # return assignment 