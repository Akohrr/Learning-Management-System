from django.contrib import admin
from accounts.models import User
from .models import Comment, Course, QuizOrAssignment, Question, Discussion
from .forms import CourseForm


admin.site.register(Comment)

admin.site.register(QuizOrAssignment)

class CourseAdmin(admin.ModelAdmin):

    form = CourseForm
    list_display = ('code', 'title',)


admin.site.register(Course, CourseAdmin)

admin.site.register(Question)


admin.site.register(Discussion)