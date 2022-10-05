from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "index.html")

def spider(request):
    return render(request, "spider.html")

def minimal(request):
    return render(request, "minimal.html")