from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import activate

def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            # Activate the language for the current request
            activate(language)
            # Create a response to redirect to the welcome page for the new language
            # The 'user:welcome' URL will now be resolved to '/fa/' or '/en/' correctly
            response = redirect(reverse('user:welcome'))
            # Set the cookie so future requests use the new language
            response.set_cookie('django_language', language)
            return response
    # Fallback redirect to the root (language selection)
    return redirect('/')