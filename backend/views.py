from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path

import os
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

# 主页
def index(request):
    return render(request, "index.html")

# 爬取数据
def spider(request):
    return render(request, "spider.html")

# 预览数据
def preview(request):
    files = os.listdir(os.path.join(BASE_DIR, 'static', 'csv'))

    try:
        filename = request.GET.get("filename")
        with open(os.path.join(BASE_DIR, 'static', 'csv', filename), 'r') as file:
            reader = csv.reader(file)
            next(reader)
            return render(request, "preview.html", locals())
    except:
        print("GG")
        return render(request, "preview.html", locals())

def minimal(request):
    return render(request, "minimal.html")