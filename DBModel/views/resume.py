import django.utils.timezone as timezone;
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from weblist.settings import HOME_URL

import datetime;

# 游戏列表
def req(request):
    workItems = [
        {
            "time" : datetime.date(2017, 7, 7),
            "description" : "主要做了什么？",
        },
        {
            "time" : datetime.date(2018, 4, 9),
            "description" : "主要做了什么？",
        },
    ];
    return render(request, "resume.html", {
        "HOME_URL": HOME_URL,
        "HEAD_TITLE" : "JinZhang-Resume",
        "TITLE" : "Resume",
        "TITLE_URL" : "http://localhost:8008/resume",
        "userInfo" : {
            "name" : "JinZhang",
            "img" : "/static/img/dzjh-icon.png",
            "phone" : "15602291936",
            "email" : "15602291936@163.com",
            "urlTitle" : "个人网站",
            "url" : "http://jimdreamheart.club",
            "gitUrlTitle" : "GitHub网址",
            "gitUrl" : "https://github.com/JDreamHeart",
        },
        "schoolInfo" : {
            "startTime" : datetime.date(2013, 9, 1),
            "endTime" : datetime.date(2017, 7, 1),
            "degree" : "本科",
            "college" : "SCNU",
            "profession" : "GD",
        },
        "workInfo" : {
            "startTime" : datetime.date(2017, 7, 7),
            "companyIcon" : "/static/img/dzjh-icon.png",
            "company" : "BY",
            "position" : "--",
            "items" : workItems,
            "itemCols" : int(12 / len(workItems)),
        },
        "projectInfo" : {
            "title" : "PyToolsIP",
            "subTitle" : "Python工具集成平台",
            "description" : """<div>
                    <p>本平台基于<a href="https://wxpython.org/" target="_blank" title="wxpython"><b>wxPython</b></a>框架开发，包含<b>Python3.7</b>版本运行库，旨在提供用户以可视化界面来使用<b>Python工具</b>。</p>
                    <p>在使用工具时，除了可使用本平台自带的工具外，还允许<b>用户开发自定义功能</b>的工具，而用户可选择将所开发的工具上传到本平台，以共享给其他人下载使用。</p>
                </div>""",
            "startTime" : datetime.date(2018, 4, 19),
        },
    });

def getResumeInfo():
    return ;