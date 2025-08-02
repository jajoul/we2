from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from .forms import SignUpStep1Form, SignUpStep2Form
from .models import User
from django.contrib.auth import authenticate, login
from insight.models import Channel

# Create your views here.
class WelcomeView(TemplateView):
    template_name = 'user/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Welcome'
        return context
class LanguageSelectionView(TemplateView):
    template_name = 'user/language_selection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Language Selection'
        return context
class LoginSignupView(TemplateView):
    template_name = 'user/login_signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login/Signup'
        return context
class SignupProcessView(View):
    def get(self, request):
        step = request.GET.get('step', '1')
        if step == '1':
            form = SignUpStep1Form(request.session.get('step1_data'))
            return render(request, 'user/signup_process.html', {'step1_form': form, 'current_step_index': 0})
        elif step == '2':
            if 'step1_data' not in request.session:
                return redirect(request.path + '?step=1')
            form = SignUpStep2Form()
            return render(request, 'user/signup_process.html', {'step2_form': form, 'current_step_index': 1})
        elif step == '3':
            # This is the success page
            return render(request, 'user/signup_process.html', {'current_step_index': 2})
        else:
            return redirect(request.path + '?step=1')

    def post(self, request):
        step = request.POST.get('step')

        if step == '1':
            form = SignUpStep1Form(request.POST)
            if form.is_valid():
                request.session['step1_data'] = form.cleaned_data
                return redirect(request.path + '?step=2')
            return render(request, 'user/signup_process.html', {'step1_form': form, 'current_step_index': 0})
        
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
                
                # Redirect to the success step
                return redirect(request.path + '?step=3')
            
            return render(request, 'user/signup_process.html', {'step2_form': form, 'current_step_index': 1})

        # If the final form is submitted (from step 3)
        elif step == '3':
            # The user is already created, so just redirect to the login page
            return redirect('user:login-signup')

        return redirect(request.path + '?step=1')
class LoginView(View):
    def get(self, request):
        return render(request, 'user/login_page.html')

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
            pass  # Fall through to the error message
        
        return render(request, 'user/login_page.html', {'error_message': 'Invalid email or password.'})

class DashboardView(TemplateView):
    template_name = 'user/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channels'] = Channel.objects.order_by('-created_at')[:10]
        return context
        