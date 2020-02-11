import django.utils.timezone as timezone;
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from DBModel import models;
from weblist.settings import HOME_URL, RESOURCE_URL;

import datetime;

from _Global import _GG;

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

# 简历请求
@csrf_exempt
def req(request):
    reqFailedTips = ""; # 请求失败提示
    try:
        token = request.GET.get("token", "");
        rt = models.ResumeToken.objects.get(token = token);
        if rt.expires > 0: # 校验简历token
            targetTime = rt.active_at + datetime.timedelta(days = rt.expires);
            delta = targetTime - timezone.now();
            leftDays = delta.days + delta.seconds / 86400;
            if leftDays > 0:
                resumeInfo = getResumeInfo();
                resumeInfo["HOME_URL"] = HOME_URL;
                resumeInfo["RESOURCE_URL"] = RESOURCE_URL;
                resumeInfo["HOME_TITLE"] = "JDreamHeart";
                return render(request, "resume/index.html", resumeInfo);
    except Exception as e:
        _GG("Log").e(f"Invalid resume token! Err[{e}]!");
        reqFailedTips = "输入的Token无效！请重试！";
    return render(request, "resume/login.html", {
        "HOME_URL" : HOME_URL,
        "RESOURCE_URL" : RESOURCE_URL,
        "HOME_TITLE" : "JDreamHeart",
        "HEAD_TITLE" : "Login-Resume",
        "requestFailedTips" : reqFailedTips,
    });

def getResumeInfo():
    return {
        "HEAD_TITLE" : "JinZhang-Resume",
        "userInfo" : {
            "name" : "JinZhang",
            "img" : "/static/img/dzjh-icon.png",
            "kvList" : [
                {"k" : "Phone", "v" : "15602291936"},
                {"k" : "Email", "v" : "manager@jdreamheart.com"},
                {"k" : "MyWeb", "v" : "https://jdreamheart.com", "vt" : "a"},
                {"k" : "GitHub", "v" : "https://github.com/JDreamHeart", "vt" : "a"},
            ],
        },
        "infoList" : [
            {
                "type" : "school",
                "name" : "学历信息",
                "items" : [
                    {
                        "startTime" : datetime.date(2013, 9, 1),
                        "endTime" : datetime.date(2017, 7, 1),
                        "degree" : "本科",
                        "college" : "SCNU",
                        "profession" : "GD",
                    },
                    {
                        "startTime" : datetime.date(2013, 9, 1),
                        "endTime" : datetime.date(2017, 7, 1),
                        "degree" : "本科",
                        "college" : "SCNU",
                        "profession" : "GD",
                    },
                ],
            },
            {
                "type" : "project",
                "name" : "实践项目",
                "items" : [
                    {
                        "title" : "PyToolsIP",
                        "subTitle" : "Python工具集成平台",
                        "description" : """<div>
                                <p>本平台基于<a href="https://wxpython.org/" target="_blank" title="wxpython"><b>wxPython</b></a>框架开发，包含<b>Python3.7</b>版本运行库，旨在提供用户以可视化界面来使用<b>Python工具</b>。</p>
                                <p>在使用工具时，除了可使用本平台自带的工具外，还允许<b>用户开发自定义功能</b>的工具，而用户可选择将所开发的工具上传到本平台，以共享给其他人下载使用。</p>
                            </div>""",
                        "startTime" : datetime.date(2018, 4, 19),
                    },
                    {
                        "title" : "PyToolsIP",
                        "subTitle" : "Python工具集成平台",
                        "description" : """<div>
                                <p>本平台基于<a href="https://wxpython.org/" target="_blank" title="wxpython"><b>wxPython</b></a>框架开发，包含<b>Python3.7</b>版本运行库，旨在提供用户以可视化界面来使用<b>Python工具</b>。</p>
                                <p>在使用工具时，除了可使用本平台自带的工具外，还允许<b>用户开发自定义功能</b>的工具，而用户可选择将所开发的工具上传到本平台，以共享给其他人下载使用。</p>
                            </div>""",
                        "startTime" : datetime.date(2018, 4, 19),
                    },
                ],
            },
            {
                "type" : "work",
                "name" : "工作经历",
                "items" : [
                    {
                        "startTime" : datetime.date(2017, 7, 7),
                        "companyIcon" : "/static/img/dzjh-icon.png",
                        "company" : "BY",
                        "position" : "--",
                        "items" : workItems,
                        "itemCols" : int(12 / len(workItems)),
                    },
                    {
                        "startTime" : datetime.date(2017, 7, 7),
                        "companyIcon" : "/static/img/dzjh-icon.png",
                        "company" : "BY",
                        "position" : "--",
                        "items" : workItems,
                        "itemCols" : int(12 / len(workItems)),
                    },
                ],
            },
        ],
    };