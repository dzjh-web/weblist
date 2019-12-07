import django.utils.timezone as timezone;
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from weblist.settings import HOME_URL

# 游戏列表
def req(request):
    return render(request, "resume.html", {
        "HOME_URL": HOME_URL,
        "TITLE" : "Resume",
        "TITLE_URL" : "http://localhost:8008/resume",
        "resumeInfo" : getResumeInfo(),
    });

def getResumeInfo():
    return {};