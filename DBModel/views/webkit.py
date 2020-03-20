from django.views.decorators.csrf import csrf_exempt;
from django.shortcuts import render;

from DBModel import models;

from weblist.settings import HOME_URL, RESOURCE_URL;

from release.base import WebType, Status;

webTypeTitleMap = {
    "github" : "Github",
    "wiki" : "文档",
};

resultKeyMap = {
    "github" : "cardlist",
    "wiki" : "cardlist_hover",
};

# 网页列表
@csrf_exempt
def req(request):
    webType = request.GET.get("t", "wiki");
    wtype = WebType.Wiki.value;
    if webType == "github":
        wtype = WebType.Github.value;
    title = webTypeTitleMap.get(webType, "网页");
    # 返回url列表
    reqKey = request.GET.get("k", "");
    if reqKey == "search":
        return search(request, webType, wtype, title);
    isHasInfo, infoList = getWebInfoList(wtype);
    return render(request, "webkit.html", {
        "HOME_URL": HOME_URL,
        "RESOURCE_URL" : RESOURCE_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE" : title + "列表",
        "TITLE" : title + "列表",
        "TITLE_URL" : f"{HOME_URL}/web?t={webType}",
        "SEARCH_URL" : f"{HOME_URL}/web?t={webType}&k=search",
        "SEARCH_KEY" : title,
        "placeholder" : f"搜索{title}名称",
        "carouselList" : getCarouseList(wtype),
        "hasInfo" : isHasInfo,
        "infoList" : infoList,
        "resultKey" : resultKeyMap.get(webType, "cardlist"),
    });

# 获取轮播列表
def getCarouseList(wtype):
    infoList = models.Carouse.objects.filter(wtype = wtype, state = Status.Open.value).order_by("-sort_id", "-update_time");
    return [{
        "name" : info.name,
        "title" : info.title,
        "url" : info.url,
        "img" : info.img.url,
        "alt" : info.alt,
        "time" : info.time,
        "update_time" : info.update_time,
    } for info in infoList];

# 获取网页信息列表
def getWebInfoList(wtype, nameText = ""):
    infoList = models.WebItem.objects.filter(name__icontains = nameText, wtype = wtype, state = Status.Open.value).order_by("-sort_id", "-update_time");
    return len(infoList) > 0, [{
        "title" : info.name,
        "subTitle" : info.title,
        "thumbnail" : info.thumbnail.url,
        "description" : info.description,
        "url" : info.url,
        "time" : info.time,
        "updateTime" : info.update_time,
    } for info in infoList];

# 搜索网页
def search(request, webType, wtype, title):
    searchText = request.POST.get("searchText", "");
    isHasInfo, infoList = getWebInfoList(wtype, searchText);
    return render(request, "webkit.html", {
        "HOME_URL": HOME_URL,
        "RESOURCE_URL" : RESOURCE_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE" : title + "列表-搜索",
        "TITLE" : title + "列表",
        "TITLE_URL" : f"{HOME_URL}/web?t={webType}",
        "hasInfo" : isHasInfo,
        "infoList" : infoList,
        "resultKey" : resultKeyMap.get(webType, "cardlist"),
        "searchInfo" : {
            "key" : title,
            "type" : "名称",
            "value" : searchText,
            "placeholder" : f"搜索{title}名称",
        },
    });