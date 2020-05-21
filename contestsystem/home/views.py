from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Announcement
from .forms import RegistrationForm

# Create your views here.

def index(req):
    data = {'Announcements': Announcement.objects.all().order_by('-date')}
    return render(req, 'pages/home.html', data)

def register(req):
    form = RegistrationForm()
    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(req, 'pages/register.html', {'form': form})
