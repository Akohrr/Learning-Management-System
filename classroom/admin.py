from django.contrib import admin
from accounts.models import User
from .models import Comment, Course, QuizOrAssignment, Question, Discussion, Grade
from .forms import CourseForm


admin.site.register(Comment)

class CourseAdmin(admin.ModelAdmin):

    form = CourseForm
    list_display = ('code', 'title',)

class QuizOrAssignmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner',)

admin.site.register(QuizOrAssignment, QuizOrAssignmentAdmin)


admin.site.register(Course, CourseAdmin)

admin.site.register(Question)


admin.site.register(Discussion)

admin.site.register(Grade)