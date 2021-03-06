from django.views.decorators.csrf import csrf_exempt;
from django.db.models import Q;
import django.utils.timezone as timezone;
from django.http import JsonResponse;
from django.shortcuts import render;

from DBModel import models;

from weblist.settings import HOME_URL, RESOURCE_URL;

from release.base import WebType, Status, Schedule, ScheduleMap;

import webkit;

from _Global import _GG;

# 游戏列表
@csrf_exempt
def req(request):
    reqKey = request.GET.get("k", "");
    if reqKey == "detail":
        return detail(request);
    elif reqKey == "log":
        return gameLog(request);
    elif reqKey == "search":
        return search(request);
    # 返回游戏列表数据
    isHasInfo, infoList = getGameInfoList();
    return render(request, "webkit.html", {
        "HOME_URL": HOME_URL,
        "RESOURCE_URL" : RESOURCE_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE": "游戏列表",
        "TITLE" : "游戏列表",
        "TITLE_URL" : f"{HOME_URL}/game",
        "SEARCH_URL" : f"{HOME_URL}/game?k=search",
        "SEARCH_KEY" : "游戏",
        "placeholder" : "搜索游戏名称",
        "carouselList" : getCarouseList(),
        "hasInfo" : isHasInfo,
        "infoList" : infoList,
        "resultKey" : "itemlist",
    });

# 游戏详情
def detail(request):
    request.encoding = "utf-8";
    _GG("Log").d("detail GET :", request.GET, "; POST :", request.POST, "; FILES :", request.FILES);
    if "searchLog" in request.GET:
        return searchLog(request);
    # 返回详情
    result = {
        "HOME_URL": HOME_URL,
        "RESOURCE_URL" : RESOURCE_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE": "GameDetail",
        "TITLE" : "游戏列表",
        "TITLE_URL" : f"{HOME_URL}/game",
        "SEARCH_URL" : f"{HOME_URL}/game?k=search",
        "searchKey" : "游戏",
        "placeholder" : "搜索游戏名称",
        "logPlaceholder" : "搜索游戏日志名称",
        "hasInfo" : False,
    };
    try:
        # 获取相应游戏信息
        gid = int(request.GET.get("gid", "0"));
        info = models.GameItem.objects.get(id = gid);
        # 返回游戏信息
        if "gameinfo" in request.GET:
            return JsonResponse(getGameInfoByItem(info, request.GET["gameinfo"]));
        # 校验游戏
        if info.state == Status.Open.value or info.token == request.GET.get("token", "game_token"):
            # 返回游戏详情页
            result["gid"] = gid;
            result["hasInfo"] = True;
            result["HEAD_TITLE"] = info.name;
            result["detailInfo"] = {
                "name" : info.name,
                "category" : info.category,
                "thumbnail" : info.thumbnail.url,
                "description" : info.description,
                "filePath" : info.file_path and info.file_path.url or "",
                "demoVideo" : info.demo_video,
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
            if info.file_path or info.demo_video:
                result["detailInfo"]["hasGameContent"] = True;
            # 获取游戏日志信息
            logurl = f"{HOME_URL}/game?k=log&gid=";
            infoList = models.GameLog.objects.filter(gid = info).order_by("-update_time");
            result["logInfoList"] = [{
                "title" : logInfo.title,
                "subTitle" : logInfo.sub_title,
                "sketch" : logInfo.sketch,
                "url" : info.state == Status.Open.value and f"{logurl}{logInfo.id}" or f"{logurl}{logInfo.id}&token={info.token}",
                "time" : logInfo.time,
                "updateTime" : logInfo.update_time,
                "exinfoList" : [],
            } for logInfo in infoList];
            result["hasLogInfo"] = len(result["logInfoList"]) > 0;
    except Exception as e:
        _GG("Log").w(e);
    return render(request, "game_detail.html", result);

# 获取轮播列表
def getCarouseList():
    return webkit.getCarouseList(WebType.Game.value);

# 搜索日志
def searchLog(request):
    searchText = request.GET.get("searchLog", "");
    result = {"htmlData" : "<p class='text-center'>数据异常，请重试！</p>"};
    try:
        # 获取相应游戏信息
        gid = int(request.POST.get("gid", "0"));
        gi = models.GameItem.objects.get(id = gid);
        # 校验游戏
        if gi.state == Status.Open.value or gi.token == request.GET.get("token", "game_token"):
            # 获取游戏日志信息
            logurl = f"{HOME_URL}/game?k=log&gid=";
            infoList = models.GameLog.objects.filter(Q(title__icontains = searchText) | Q(sub_title__icontains = searchText), gid = gi).order_by("-update_time");
            result["htmlData"] = bytes.decode(render(request, "gamelog_list.html", {
                "searchText" : searchText,
                "logInfoList" : [{
                    "title" : logInfo.title,
                    "subTitle" : logInfo.sub_title,
                    "sketch" : logInfo.sketch,
                    "url" : gi.state == Status.Open.value and f"{logurl}{logInfo.id}" or f"{logurl}{logInfo.id}&token={gi.token}",
                    "time" : logInfo.time,
                    "updateTime" : logInfo.update_time,
                    "exinfoList" : [],
                } for logInfo in infoList],
                "hasLogInfo" : len(infoList) > 0,
            }).content);
    except Exception as e:
        _GG("Log").w(e);
    return JsonResponse(result);

# 游戏日志详情
def gameLog(request):
    # 返回详情
    result = {
        "HOME_URL": HOME_URL,
        "RESOURCE_URL" : RESOURCE_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE": "GameDetail",
        "TITLE" : "游戏列表",
        "TITLE_URL" : f"{HOME_URL}/game",
        "SEARCH_URL" : f"{HOME_URL}/game?k=search",
        "placeholder" : "搜索游戏名称",
        "hasInfo" : False,
    };
    try:
        # 获取相应游戏信息
        gid = int(request.GET.get("gid", "0"));
        info = models.GameLog.objects.get(id = gid);
        # 校验游戏
        if info.gid.state == Status.Open.value or info.gid.token == request.GET.get("token", "game_token"):
            result["gid"] = gid;
            result["hasInfo"] = True;
            result["HEAD_TITLE"] = info.title;
            result["gameInfo"] = {
                "url" : f"{HOME_URL}/game?k=detail&gid=" + str(info.gid.id),
                "name" : info.gid.name,
                "category" : info.gid.category,
            };
            result["detailInfo"] = {
                "title" : info.title,
                "subTitle" : info.sub_title,
                "time" : info.time,
                "updateTime" : info.update_time,
                "content" : info.cid.content,
            };
    except Exception as e:
        _GG("Log").w(e);
    return render(request, "gamelog_detail.html", result);

# 获取游戏信息列表
def getGameInfoList(nameText = ""):
    infoList = models.GameItem.objects.filter(name__icontains = nameText, state = Status.Open.value).order_by("-sort_id", "-update_time");
    return len(infoList) > 0, [{
        "title" : info.name,
        "subTitle" : info.category,
        "thumbnail" : info.thumbnail.url,
        "description" : info.description,
        "url" : f"{HOME_URL}/game?k=detail&gid={info.id}",
        "time" : info.time,
        "updateTime" : info.update_time,
        "exinfoList" : [{"key" : "进度", "value" : info.schedule}],
    } for info in infoList];

# 搜索游戏
def search(request):
    searchText = request.POST.get("searchText", "");
    isHasInfo, infoList = getGameInfoList(searchText);
    return render(request, "webkit.html", {
        "HOME_URL": HOME_URL,
        "RESOURCE_URL" : RESOURCE_URL,
        "HOME_TITLE": "JDreamHeart",
        "HEAD_TITLE": "游戏列表-搜索",
        "TITLE" : "游戏列表",
        "TITLE_URL" : f"{HOME_URL}/game",
        "hasInfo" : isHasInfo,
        "infoList" : infoList,
        "resultKey" : "itemlist",
        "searchInfo" : {
            "key" : "游戏",
            "type" : "名称",
            "value" : searchText,
            "placeholder" : "搜索游戏名称",
        },
    });

# 获取游戏信息
def getGameInfoByItem(gameItem, infoType):
    if infoType == "version":
        if gameItem.file_path:
            return {
                "version" : gameItem.version or "0.0",
                "url" : HOME_URL + gameItem.file_path.url,
                "size" : gameItem.file_path.size,
            };
    return {};