import os, string, random
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from .models import Problems, Submission

securityTokenLength = 20

def genToken(len = securityTokenLength):
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=len))

# Create your views here.
def index(req):
    return HttpResponseRedirect('problems')

def problems(req):
    data = {'problems': Problems.objects.all().order_by("title")}
    return render(req, 'pages/problems.html', data)

def problemsList(req, codename):
    data = {'req_problem': Problems.objects.get(title = codename)}
    if req.method == 'POST' and req.FILES['submission']:
        sourceCode = req.FILES['submission']
        fs = FileSystemStorage()
        realSourceCodeName, ext = os.path.splitext(sourceCode.name)
        token = genToken()
        filename = fs.save(f"contestant_solutions/{realSourceCodeName}_{req.user}_{codename}_{token}.{ext}", sourceCode)
        upload_to = fs.url(filename)
        return HttpResponseRedirect('../submissions')
    return render(req, 'pages/problems.html', data)

def submit(req):
    return render(req, 'pages/submit.html')

def submissions(req):
    data = {'Submissions': Submission.objects.filter(user = req.user).order_by("-id")}
    return render(req, 'pages/submissions.html', data)

def standings(req):
    return render(req, 'pages/standings.html')