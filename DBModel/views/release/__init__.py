from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.core.mail import send_mail

from weblist.settings import HOME_URL
from DBModel import models
from utils import base_util

import hashlib;
import os,sys;

from _Global import _GG;

from release.base import WebType;
from release import web_item, game_item, game_log;

# 键值列表
keyList = ["add_home_url", "operate_home_url", "add_wiki", "operate_wiki", "add_github", "operate_github"];
gameList = ["add_game", "operate_game", "add_game_log", "operate_game_log"];

# 后台管理页请求
@csrf_exempt
def release(request):
    _GG("Log").d(request.method, "release get :", request.GET, "release post :", request.POST, "release files :", request.FILES);
    # 判断是否校验
    if "isVerify" in request.POST:
        return verify(request);
    # 判断是否已登陆
    if request.method == 'GET':
        return render(request, "release/index.html", {"HOME_URL": HOME_URL});
    # 获取登陆玩家
    userAuth = request.userAuth;
    if not userAuth:
        # 返回登陆页面信息
        ret = {"HOME_URL": HOME_URL};
        return render(request, "release/login.html", ret);
    # 是否切换Tab
    isSwitchTab = base_util.getPostAsBool(request, "isSwitchTab");
    # 获取请求键值
    mkey = request.POST.get("mk", "");
    # 判断是否重定向
    if mkey not in keyList or mkey not in gameList:
        # 重置mkey
        mkey = keyList[0];
        isSwitchTab = True;
    # 返回管理项的内容
    return render(request, "release/item.html", getReleaseResult(request, userAuth, mkey, isSwitchTab));

# 校验逻辑
def verify(request):
    # 校验游戏名
    if "gameName" in request.POST:
        if len(models.GameItem.objects.filter(name = request.POST["gameName"])) == 0:
            return HttpResponse("true");
    # 校验失败
    _GG("Log").d("Verify Fail!", request.POST);
    return HttpResponse("false");

# 获取管理页返回结果
def getReleaseResult(request, userAuth, mkey, isSwitchTab):
    # 返回页面内容
    result = {
        "HOME_URL": HOME_URL,
        "mkey" : mkey,
        "requestTips" : "", # 请求提示
        "requestFailedTips" : "", # 请求失败提示
        "onlineInfoList" : [], # 线上信息列表
    };
    if mkey == "add_home_url": # 新增首页网站
        web_item.upload(request, userAuth, result, isSwitchTab, WebType.Home.value);
    elif mkey == "operate_home_url": # 操作首页网站
        web_item.update(request, userAuth, result, isSwitchTab, WebType.Home.value);
    elif mkey == "add_wiki": # 新增文档信息
        web_item.upload(request, userAuth, result, isSwitchTab, WebType.Wiki.value);
    elif mkey == "operate_wiki": # 操作文档信息
        web_item.update(request, userAuth, result, isSwitchTab, WebType.Wiki.value);
    elif mkey == "add_github": # 新增Github信息
        web_item.upload(request, userAuth, result, isSwitchTab, WebType.Github.value);
    elif mkey == "operate_github": # 操作Github信息
        web_item.update(request, userAuth, result, isSwitchTab, WebType.Github.value);
    # 以下为游戏相关内容
    elif mkey == "add_game": # 新增游戏信息
        game_item.upload(request, userAuth, result, isSwitchTab, WebType.Wiki.value);
    elif mkey == "operate_game": # 操作游戏信息
        game_item.update(request, userAuth, result, isSwitchTab, WebType.Wiki.value);
    elif mkey == "add_game_log": # 新增游戏日志
        game_log.upload(request, userAuth, result, isSwitchTab, WebType.Github.value);
    elif mkey == "operate_game_log": # 操作游戏日志
        game_log.update(request, userAuth, result, isSwitchTab, WebType.Github.value);
    return result;
