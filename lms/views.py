from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return redirect('accounts:login')


@login_required
def home_page(request):
    try:
        if request.user.user_type == 'LA':
            return redirect("classroom:lms_admin_view", choice='lms_admins')

        elif request.user.user_type == 'IN':
            return redirect("classroom:instructor_view", choice='assignments')

        elif request.user.user_type == 'ST':
            return redirect("classroom:student_view", choice='courses')

        else:
            raise PermissionDenied
    
    except AttributeError:
  
        return redirect('accounts:login')
