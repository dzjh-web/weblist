import django.utils.timezone as timezone;
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from DBModel import models;
from weblist.settings import HOME_URL, RESOURCE_URL;

import os;
import json;
import datetime;

from _Global import _GG;


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
                resumeInfo = getResumeInfo(rt.remarks);
                if resumeInfo:
                    resumeInfo["HOME_URL"] = HOME_URL;
                    resumeInfo["RESOURCE_URL"] = RESOURCE_URL;
                    resumeInfo["HOME_TITLE"] = "JDreamHeart";
                    return render(request, "resume/index.html", resumeInfo);
                else:
                    reqFailedTips = "对应Token的remarks（备注）无效！获取简历信息失败！";
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

# 获取简历信息
def getResumeInfo(remarks = "resume"):
    filePath = os.path.join(_GG("ProjectPath"), "assets", "static", "json", "resume", remarks+".json");
    if os.path.exists(filePath):
        try:
            with open(filePath, "rb") as f:
                info = json.loads(f.read().decode("utf-8"));
                for itemInfo in info.get("infoList", []):
                    if itemInfo.get("type", "") == "work":
                        for item in itemInfo.get("items", []):
                            workItems = item.get("items", []);
                            if len(workItems) > 0:
                                item["itemCols"] = int(12 / len(workItems));
                    pass;
                return info;
        except Exception as e:
            _GG("Log").e(f"Invalid resume remarks! Err[{e}]!");
    return {};