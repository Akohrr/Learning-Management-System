from django.shortcuts import render, redirect


def landing_page(request):
    return redirect('accounts:login')