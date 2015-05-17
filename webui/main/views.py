import glob
from django.shortcuts import render

# Create your views here.

def index(request):
    context = {'info': 'data'}
    return render(request, 'index.html', context)

def contents(request, path):
    context = {
        'data': glob.glob(path),
    }
    return render(request, 'contents.html', context)