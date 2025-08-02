from django.urls import path
from . import views

app_name = 'insight'

urlpatterns = [
    path('base/', views.base, name='base'),
    path('create_channel/', views.CreateChannelView.as_view(), name='create_channel'),
    path('channel/<int:pk>/', views.ChannelDetailView.as_view(), name='channel_detail'),
]