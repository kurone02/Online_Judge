from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Problems

# Create your views here.
def index(req):
    return HttpResponseRedirect('problems')

def problems(req):
    data = {'problems': Problems.objects.all()}
    return render(req, 'pages/problems.html', data)

def problemsList(req, codename):
    data = {'req_problem': Problems.objects.get(title = codename)}
    return render(req, 'pages/problems.html', data)

def submit(req):
    return render(req, 'pages/submit.html')

def submissions(req):
    return render(req, 'pages/submissions.html')

def standings(req):
    return render(req, 'pages/standings.html')