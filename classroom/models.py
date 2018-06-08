from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
# Create your models here.


class Module(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField()
    class_file = models.FileField()

    def __str__(self):
        return self.name         



#modules refers to content of the course 
class Course(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=6, unique=True, primary_key=True)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='instructors')
    syllabus = models.TextField()
    modules = models.ManyToManyField(Module)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students')
    teaching_assistants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teaching_assistant', blank=True)


    def __str__(self):
        return '{0}'.format(self.code)




#used to handle both quiz and assignments
class QuizOrAssignment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_of_submission = models.DateTimeField(help_text='Date and time of submission')
    is_assignment = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('classroom:instructor_add_choice', kwargs={'choice':'quiz', 'pk': self.pk })

    class Meta:
        permissions = (
            ('modify_quiz_or_assignment', 'Modify quiz or assignment'),
        )

        
class Question(models.Model):
    quiz_or_assignment = models.ForeignKey(QuizOrAssignment, on_delete=models.CASCADE)
    text = models.TextField('Question')
    first_option = models.TextField('A')
    second_option = models.TextField('B')
    third_option = models.TextField('C')
    fourth_option = models.TextField('D')
    answer = models.TextField()
    def __str__(self):
        return self.text


class Grade(models.Model):
    score = models.DecimalField(default=0, decimal_places=2, max_digits=100, help_text='Score is expressed in percentage')
    quiz_or_assignment = models.ForeignKey(QuizOrAssignment, on_delete=models.CASCADE, null=True, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.username

class Discussion(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #choice represents discussion
        return reverse('classroom:instructor_add_choice', kwargs={'choice':'discussion', 'pk': self.pk })


class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, default=None, null=True)
    created = models.DateTimeField(auto_now=True)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    def __str__(self):
        return self.body