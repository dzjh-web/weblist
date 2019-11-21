import django.utils.timezone as timezone;
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# 游戏列表
def req(request):
    return render(request, "itemlist.html", {
        "TITLE" : "Games",
        "TITLE_URL" : "http://localhost:8008/games",
        "SEARCH_URL" : "http://localhost:8008/search?k=game",
        "searchText" : "搜索游戏名称",
        "infoList" : getGameList(),
        "carouselList" : getCarouseList(),
    });

# 游戏详情
def detail(request):
    return render(request, "detail.html", {
        "TITLE" : "Game",
        "TITLE_URL" : "http://localhost:8008/games",
        "SEARCH_URL" : "http://localhost:8008/search?k=game",
        "searchText" : "搜索游戏名称",
        "hasInfo" : True,
        "infoList" : getGameList(),
        "detailInfo" : {
            "name" : "游戏名称",
            "title" : "标题",
            "time" : timezone.now(),
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "<p>游戏介绍</p>",
            "schedule" : "计划中",
        },
        "logInfoList" : [
            {
                "url" : "xxx?id=233",
                "title" : "标题",
                "subTitle" : "子标题",
                "content" : "<p>日志内容</p>",
                "time" : timezone.now(),
                "exinfoList" : [],
            },
            {
                "url" : "xxx?id=666",
                "title" : "标题",
                "content" : "<p>日志内容</p>",
                "time" : timezone.now(),
                "exinfoList" : [],
            },
        ],
    });

# 获取游戏列表
def getGameList():
    return [
        {
            "title" : "test",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "只是测试用的。。。",
            "url" : "http://localhost:8008/games",
            "time" : timezone.now(),
            "exinfoList" : [{"key" : "进度", "value" : "计划中"}],
        },
        {
            "title" : "test2",
            "subTitle" : "xxxtest2",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "鼎折覆餗",
            "url" : "http://localhost:8008/games",
            "time" : timezone.now(),
            "exinfoList" : [{"key" : "进度", "value" : "筹备中"}],
        },
    ];

# 获取轮播列表
def getCarouseList():
    return [
        {
            "name" : "test",
            "img" : "/media/home/img/pytoolsip.png",
            "alt" : "test",
            "url" : "===========",
            "title" : "xxxxxxxxx",
        },
        {
            "name" : "test233",
            "img" : "/media/home/img/pytoolsip.png",
            "alt" : "test233",
            "url" : "=====-------======",
            "title" : "xxxxx=======xxxx",
        },
    ];