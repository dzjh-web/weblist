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

from release import home_list;

# 键值列表
keyList = ["add_home_url", "operate_home_url", "add_game", "operate_game", "add_game_log", "operate_game_log", "add_gitbook", "operate_gitbook", "add_gitbook", "operate_gitbook"];

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
    if mkey not in keyList:
        # 重置mkey
        mkey = keyList[0];
        isSwitchTab = True;
    # 返回管理项的内容
    return render(request, "release/item.html", getReleaseResult(request, userAuth, mkey, isSwitchTab));

# 校验逻辑
def verify(request):
    # 校验网站名
    if "webname" in request.POST:
        if len(models.WebItem.objects.filter(name = request.POST["webname"])) == 0:
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
    if mkey == "add_home_url": # (首页)新增网页链接
        ptip.examine(request, userAuth, result, isSwitchTab);
    return result;
