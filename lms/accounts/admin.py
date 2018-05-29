from django.contrib import admin
from django.conf import settings
from .forms import UserCreationForm

from .models import User
#register your models here.

class UserAdmin(admin.ModelAdmin):
    # form = UserCreationForm
    list_filter = ('user_type',)
    list_display = ('first_name', 'last_name', 'username', 'email', 'user_type',)

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', )
    #     })
    # )


admin.site.register(User, UserAdmin)