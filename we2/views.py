from django.shortcuts import render, redirect
from django.utils.translation import activate, get_language
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            request.session['django_language'] = language
            activate(language)
    return redirect(request.POST.get('next', '/'))