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

class Grade(models.Model):
    GRADE_CHOICES = (
        ('A', 'A(80-100)'),
        ('B', 'B(70-79)'),
        ('C', 'C(60-69)'),
        ('D', 'D(50-59)'),
        ('E', 'E(40-49)'),
        ('F', 'F(30-39)'),
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)




class Comment(models.Model):
    created = models.DateTimeField(auto_now=True)
    body = models.TextField()
    author = models.OneToOneField(settings.AUTH_USER_MODEL)


#used to handle both quiz and assignments
class QuizOrAssignment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.ManyToManyField(Comment, blank=True)
    date_of_submission = models.DateTimeField(help_text='Date and time of submission')
    is_assignment = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('classroom:instructor_add_question', kwargs={'choice':'quiz', 'pk': self.pk })
    
    def get_absolute_url_student(self):
        pass
class Question(models.Model):
    quiz = models.ForeignKey(QuizOrAssignment, on_delete=models.CASCADE)
    text = models.TextField('Question')
    first_option = models.TextField('A')
    second_option = models.TextField('B')
    third_option = models.TextField('C')
    fourth_option = models.TextField('D')
    answer = models.TextField()
    def __str__(self):
        return self.text


class Discussion(models.Model):
    title = models.CharField(max_length=30)
    comments = models.OneToOneField(Comment, on_delete=models.CASCADE)
    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title