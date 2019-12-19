from django.shortcuts import render;

from DBModel import models;

from weblist.settings import HOME_URL;

from release.base import WebType, Status;

# url列表
def req(request):
    webKey = request.GET.get("k", "wiki");
    wtype = WebType.Wiki.value;
    if webKey == "github":
        wtype = WebType.Github.value;
    return render(request, "cardlist_hover.html", {
        "HOME_URL": HOME_URL,
        "TITLE" : webKey.capitalize(),
        "TITLE_URL" : f"http://localhost:8008/web?k={webKey}",
        "SEARCH_URL" : f"http://localhost:8008/search?k={webKey}",
        "searchText" : f"搜索{webKey}名称",
        "infoList" : getUrlList(wtype),
        "carouselList" : getCarouseList(wtype),
    });

# 获取游戏列表
def getUrlList(wtype):
    infoList = models.WebItem.objects.filter(wtype = wtype, state = Status.Open.value).order_by("-update_time");
    return [{
        "name" : info.name,
        "title" : info.title,
        "thumbnail" : info.thumbnail.url,
        "description" : info.description,
        "url" : info.url,
        "time" : info.time,
        "updateTime" : info.update_time,
    } for info in infoList];

# 获取轮播列表
def getCarouseList(wtype):
    infoList = models.Carouse.objects.filter(wtype = wtype, state = Status.Open.value).order_by("-update_time");
    return [{
        "name" : info.name,
        "title" : info.title,
        "url" : info.url,
        "img" : info.img.url,
        "alt" : info.alt,
        "time" : info.time,
        "update_time" : info.update_time,
    } for info in infoList];