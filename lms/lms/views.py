from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import Http404


def landing_page(request):
    if request.user.user_type == 'LA':
        return redirect(r"classroom:lms_admin_view choice='lms_admins'")

    elif request.user.user_type == 'IN':
        return redirect(r"classroom:instructor_view' choice='assignments'")

    elif request.user.user_type == 'ST':
        return redirect(r"classroom:student_view' choice='courses' ")

    else:
        raise Http404
