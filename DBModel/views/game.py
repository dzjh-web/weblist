import django.utils.timezone as timezone;
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# 首页
def req(request):
    return render(request, "itemlist.html", {
        "TITLE" : "Games",
        "TITLE_URL" : "http://localhost:8008/games",
        "SEARCH_URL" : "http://localhost:8008/search?k=game",
        "searchText" : "搜索游戏名称",
        "infoList" : getGameList(),
        "carouselList" : getCarouseList(),
    });

# 获取游戏列表
def getGameList():
    return [
        {
            "title" : "test",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "只是测试用的。。。",
            "time" : timezone.now(),
            "exinfoList" : [{"key" : "进度", "value" : "计划中"}],
        },
        {
            "title" : "test2",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "鼎折覆餗",
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