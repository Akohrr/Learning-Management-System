from django.contrib import admin
from .models import Comments, Course
from .forms import AddCourseForm
# Register your models here.

admin.site.register(Comments)


class CouseAdmin(admin.ModelAdmin):
    form = AddCourseForm


admin.site.register(Course, CouseAdmin)

# admin.site.register(Content)