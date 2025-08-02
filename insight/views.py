from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ChannelForm
from .models import Channel

# Create your views here.
def base(request):
    return render(request, 'insight/base.html')

@method_decorator(login_required, name='dispatch')
class CreateChannelView(View):
    def get(self, request):
        form = ChannelForm()
        return render(request, 'insight/create_channel.html', {'form': form})

    def post(self, request):
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.owner = request.user
            channel.save()
            return redirect('insight:channel_detail', pk=channel.pk)  # Redirect to the new channel's page
        return render(request, 'insight/create_channel.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ChannelDetailView(View):
    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        return render(request, 'insight/channel_detail.html', {'channel': channel})

