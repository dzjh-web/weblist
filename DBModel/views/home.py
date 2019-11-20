from django.shortcuts import render

# 首页
def req(request):
    return render(request, "home.html", {
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
            "wtype" : "DzjH",
            "description" : "<p>基于<b>wxPython</b>框架开发，以提供用户可视化界面来使用<b>Python工具</b>的平台网站。</p>",
        },
        {
            "url" : "http://jimdreamheart.club/gitbook",
            "img" : "/media/home/img/gitbook.png",
            "name" : "JGitBook",
            "wtype" : "JDH",
            "description" : "<p>基于<b>GitBook</b>发布的，用于记录工作、学习或日常编程的文档网站。</p>",
        },
        {
            "url" : "http://jimdreamheart.club/github",
            "img" : "/media/home/img/github.png",
            "name" : "JGitHub",
            "wtype" : "JDH",
            "description" : "<p>个人GitHub地址。</p>",
        },
    ];