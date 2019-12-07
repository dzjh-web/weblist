from django.shortcuts import render

from weblist.settings import HOME_URL

# 首页
def req(request):
    return render(request, "home.html", {
        "HOME_URL": HOME_URL,
        "TITLE": "JDreamHeart",
        "navList" : getNavList(),
        "webList" : getWebList(),
    });

# 获取导航栏项
def getNavList():
    return [
        {
            "url" : "http://jimdreamheart.club/pytoolsip",
            "title" : "python工具集成平台",
            "name" : "PYToolsIP",
        },
        {
            "url" : "http://localhost:8008/games",
            "title" : "自制游戏",
            "name" : "JGames",
        },
        {
            "url" : "http://jimdreamheart.club/gitbook",
            "title" : "文档合集",
            "name" : "JGitBook",
        },
        {
            "url" : "http://jimdreamheart.club/github",
            "title" : "GitHub合集",
            "name" : "JGitHub",
        },
    ];

# 获取网站列表
def getWebList():
    return [
        {
            "url" : "http://jimdreamheart.club/pytoolsip",
            "img" : "/media/home/img/pytoolsip.png",
            "name" : "PYToolsIP",
            "title" : "DzjH",
            "description" : "<p>基于<b>wxPython</b>框架开发，以提供用户可视化界面来使用<b>Python工具</b>的平台网站。</p>",
        },
        {
            "url" : "http://localhost:8008/games",
            "img" : "/media/home/img/pytoolsip.png",
            "name" : "JGames",
            "title" : "DzjH",
            "description" : "<p>独立制作的相关游戏列表。</p>",
        },
        {
            "url" : "http://jimdreamheart.club/gitbook",
            "img" : "/media/home/img/gitbook.png",
            "name" : "JGitBook",
            "title" : "JDH",
            "description" : "<p>基于<b>GitBook</b>发布的，用于记录工作、学习或日常编程的文档网站。</p>",
        },
        {
            "url" : "http://jimdreamheart.club/github",
            "img" : "/media/home/img/github.png",
            "name" : "JGitHub",
            "title" : "JDH",
            "description" : "<p>个人GitHub地址。</p>",
        },
    ];