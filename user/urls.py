from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('language-selection/', views.LanguageSelectionView.as_view(), name='language-selection'),
    path('login-signup/', views.LoginSignupView.as_view(), name='login-signup'),
    path('signup-process/', views.SignupProcessView.as_view(), name='signup-process'),
    path('login/', views.LoginView.as_view(), name='login'),

]