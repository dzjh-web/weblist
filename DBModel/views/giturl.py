import django.utils.timezone as timezone;
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# url列表
def req(request):
    return render(request, "cardlist.html", {
        "TITLE" : "Urls",
        "TITLE_URL" : "http://localhost:8008/games",
        "SEARCH_URL" : "http://localhost:8008/search?k=github",
        "searchText" : "搜索github名称",
        "infoList" : getUrlList(),
        "carouselList" : getCarouseList(),
    });

# 获取游戏列表
def getUrlList():
    return [
        {
            "title" : "test",
            "subTitle" : "sub_title",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "只是测试用的。。。",
            "url" : "http://localhost:8008/games",
        },
        {
            "title" : "test2",
            "subTitle" : "sub_title",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "鼎折覆餗",
            "url" : "http://localhost:8008/games",
        },
        {
            "title" : "test3",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "鼎折覆餗",
            "url" : "http://localhost:8008/games",
        },
        {
            "title" : "test4",
            "thumbnail" : "/media/home/img/pytoolsip.png",
            "description" : "鼎折覆餗",
            "url" : "http://localhost:8008/games",
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