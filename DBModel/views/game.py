import django.utils.timezone as timezone;
from django.shortcuts import render;

from DBModel import models;

from weblist.settings import HOME_URL;

from release.base import WebType, Status, Schedule, ScheduleMap;

import webkit;

from _Global import _GG;

# 游戏列表
def req(request):
    return render(request, "itemlist.html", {
        "HOME_URL": HOME_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE": "游戏列表",
        "TITLE" : "游戏列表",
        "TITLE_URL" : "http://localhost:8008/game",
        "SEARCH_URL" : "http://localhost:8008/search?k=game",
        "searchText" : "搜索游戏名称",
        "infoList" : getGameList(),
        "carouselList" : getCarouseList(),
    });

# 游戏详情
def detail(request):
    result = {
        "HOME_URL": HOME_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE": "GameDetail",
        "TITLE" : "游戏列表",
        "TITLE_URL" : "http://localhost:8008/game",
        "SEARCH_URL" : "http://localhost:8008/search?k=game",
        "searchText" : "搜索游戏名称",
        "SEARCH_LOG_URL" : "http://localhost:8008/search?k=gamelog",
        "searchLogText" : "搜索游戏日志名称",
        "hasInfo" : False,
    };
    try:
        # 获取相应游戏信息
        gid = int(request.GET.get("gid", "0"));
        info = models.GameItem.objects.get(id = gid);
        result["hasInfo"] = True;
        result["HEAD_TITLE"] = info.name;
        result["detailInfo"] = {
            "name" : info.name,
            "category" : info.category,
            "thumbnail" : info.thumbnail.url,
            "description" : info.description,
            "filePath" : info.file_path,
            "time" : info.time,
            "updateTime" : info.update_time,
            "content" : info.cid.content,
            "schedule" : {
                "key" : ScheduleMap.get(info.schedule, "未知"),
                "val" : info.schedule,
                "items" : [{"key" : v, "val" : k, "hasLine" : True} for k,v in ScheduleMap.items() if k != Schedule.Pending.value and k != Schedule.Off.value],
            },
        };
        result["detailInfo"]["schedule"]["items"].insert(0, {"key" : ScheduleMap[Schedule.Pending.value], "val" : Schedule.Pending.value});
        result["detailInfo"]["schedule"]["items"].append({"key" : ScheduleMap[Schedule.Off.value], "val" : Schedule.Off.value});
        result["detailInfo"]["schedule"]["itemWidth"] = str(int(100 / len(result["detailInfo"]["schedule"]["items"]))) + "%";
        # 获取游戏日志信息
        infoList = models.GameLog.objects.filter(gid = info).order_by("-update_time");
        result["logInfoList"] = [{
            "title" : logInfo.title,
            "subTitle" : logInfo.sub_title,
            "sketch" : logInfo.sketch,
            "url" : f"http://localhost:8008/gamelog?gid={logInfo.id}",
            "time" : logInfo.time,
            "updateTime" : logInfo.update_time,
            "content" : logInfo.cid.content,
            "exinfoList" : [],
        } for logInfo in infoList];
    except Exception as e:
        _GG("Log").w(e);
    return render(request, "detail.html", result);

# 获取游戏列表
def getGameList():
    infoList = models.GameItem.objects.all().order_by("-sort_id", "-update_time");
    return [{
        "title" : info.name,
        "subTitle" : info.category,
        "thumbnail" : info.thumbnail.url,
        "description" : info.description,
        "url" : f"http://localhost:8008/gamedetail?gid={info.id}",
        "time" : info.time,
        "updateTime" : info.update_time,
        "exinfoList" : [{"key" : "进度", "value" : info.schedule}],
    } for info in infoList];

# 获取轮播列表
def getCarouseList():
    return webkit.getCarouseList(WebType.Game.value);