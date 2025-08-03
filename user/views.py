from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from .forms import SignUpStep1Form, SignUpStep2Form
from .models import User
from django.contrib.auth import authenticate, login
from insight.models import Channel
import json
from django.utils import translation
from django.utils.translation import gettext_lazy as _

class WelcomeView(TemplateView):
    template_name = 'user/welcome.html'

    def get_context_data(self, **kwargs):
        # The LocaleMiddleware has already set the language from the URL.
        # We use gettext_lazy (_) to mark strings for translation.
        slides_data = [
            {"image": "/static/images/ilust1.jpg", "title": _("Welcome to We Too"), "description": _("A safe space for survivors of domestic violence to connect, share, and heal.")},
            {"image": "/static/images/raise-hand.jpg", "title": _("Find Your Voice"), "description": _("Share your story, connect with others who understand, and find strength in community.")},
            {"image": "/static/images/happy-family.jpg", "title": _("You Are Not Alone"), "description": _("Join a supportive network of survivors and allies. Together, we can break the cycle of violence.")}
        ]
        # We must explicitly cast the lazy translation objects to strings here.
        slides_data_translated = [{"image": item["image"], "title": str(item["title"]), "description": str(item["description"])} for item in slides_data]

        context = super().get_context_data(**kwargs)
        context['title'] = _('Welcome')
        context['lang'] = translation.get_language()
        context['slides_data_json'] = json.dumps(slides_data_translated)
        return context

class LanguageSelectionView(TemplateView):
    template_name = 'user/language_selection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Language Selection'
        context['lang'] = translation.get_language()
        return context

class LoginSignupView(TemplateView):
    template_name = 'user/login_signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Login/Signup')
        context['lang'] = translation.get_language()
        return context

class SignupProcessView(View):
    def get(self, request, *args, **kwargs):
        step = request.GET.get('step', '1')
        context = {
            'lang': translation.get_language(),
            'current_step_index': 0
        }
        if step == '1':
            context['step1_form'] = SignUpStep1Form(request.session.get('step1_data'))
        elif step == '2':
            if 'step1_data' not in request.session:
                return redirect(request.path + '?step=1')
            context['step2_form'] = SignUpStep2Form()
            context['current_step_index'] = 1
        elif step == '3':
            context['current_step_index'] = 2
        else:
            return redirect(request.path + '?step=1')
        return render(request, 'user/signup_process.html', context)

    def post(self, request, *args, **kwargs):
        step = request.POST.get('step')
        # ... (rest of the post logic remains the same)
        if step == '1':
            form = SignUpStep1Form(request.POST)
            if form.is_valid():
                request.session['step1_data'] = form.cleaned_data
                return redirect(request.path + '?step=2')
            return render(request, 'user/signup_process.html', {'step1_form': form, 'current_step_index': 0, 'lang': translation.get_language()})
        
        elif step == '2':
            if 'step1_data' not in request.session:
                return redirect(request.path + '?step=1')
            
            form = SignUpStep2Form(request.POST, request.FILES)
            if form.is_valid():
                step1_data = request.session['step1_data']
                
                user = User.objects.create_user(
                    username=step1_data['username'],
                    password=step1_data['password'],
                    email=step1_data.get('email')
                )

                user.full_name = form.cleaned_data.get('full_name')
                user.gender = form.cleaned_data.get('gender')
                if 'profile_picture' in request.FILES:
                    user.profile_picture = request.FILES['profile_picture']
                user.save()

                del request.session['step1_data']
                
                return redirect(request.path + '?step=3')
            
            return render(request, 'user/signup_process.html', {'step2_form': form, 'current_step_index': 1, 'lang': translation.get_language()})

        elif step == '3':
            return redirect('user:login-signup')

        return redirect(request.path + '?step=1')

class LoginView(View):
    def get(self, request):
        return render(request, 'user/login_page.html', {'lang': translation.get_language()})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('user:dashboard')
        except User.DoesNotExist:
            pass
        
        return render(request, 'user/login_page.html', {'error_message': 'Invalid email or password.', 'lang': translation.get_language()})

class DashboardView(TemplateView):
    template_name = 'user/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channels'] = Channel.objects.order_by('-created_at')[:10]
        context['lang'] = translation.get_language()
        return context
