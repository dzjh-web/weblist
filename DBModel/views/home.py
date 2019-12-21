from django.shortcuts import render;

from DBModel import models;

from weblist.settings import HOME_URL;

from release.base import WebType, Status;

# 首页
def req(request):
    return render(request, "home.html", {
        "HOME_URL": HOME_URL,
        "HEAD_TITLE": "JDreamHeart",
        "TITLE": "JDreamHeart",
        "navList" : getNavList(),
        "webList" : getWebList(),
    });

# 获取导航栏项
def getNavList():
    infoList = models.Carouse.objects.filter(wtype = WebType.Home.value, state = Status.Open.value).order_by("-sort_id", "-update_time");
    return [{
        "name" : info.name,
        "title" : info.title,
        "url" : info.url,
        "img" : info.img.url,
        "alt" : info.alt,
        "time" : info.time,
        "update_time" : info.update_time,
    } for info in infoList];

# 获取网站列表
def getWebList():
    infoList = models.WebItem.objects.filter(wtype = WebType.Home.value, state = Status.Open.value).order_by("-sort_id", "-update_time");
    return [{
        "name" : info.name,
        "title" : info.title,
        "thumbnail" : info.thumbnail.url,
        "description" : info.description,
        "url" : info.url,
        "time" : info.time,
        "updateTime" : info.update_time,
    } for info in infoList];