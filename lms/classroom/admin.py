from django.contrib import admin
from .models import Comments, Course, Quiz
from .forms import CourseForm
# Register your models here.

admin.site.register(Comments)

admin.site.register(Quiz)

class CouseAdmin(admin.ModelAdmin):
    form = CourseForm


admin.site.register(Course, CouseAdmin)

# admin.site.register(Content)