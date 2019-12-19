from django.db.models import Q;
import django.utils.timezone as timezone;
from django.forms import ModelForm;

from DBModel import models;
from utils import base_util;
from release.base import WebType, Status;

import json;

from _Global import _GG;

webTypeTitleMap = {
    WebType.Home.value : "首页轮播图",
    WebType.Github.value : "Github轮播图",
    WebType.Wiki.value : "文档轮播图",
    WebType.Game.value : "游戏轮播图",
};

# 轮播图表单
class CarouseForm(ModelForm):
    class Meta:
        model = models.Carouse
        fields = ["name", "title", "url", "img", "alt"]

# 上传轮播图信息
def upload(request, result, isSwitchTab, wtype = 0):
    result["title"] = webTypeTitleMap.get(wtype, "轮播图");
    if not isSwitchTab:
        isRelease = base_util.getPostAsBool(request, "isRelease");
        if isRelease:
            cf = CarouseForm(request.POST, request.FILES);
            if cf.is_valid():
                c = models.Carouse(**{
                    "name" : cf.cleaned_data["name"],
                    "title" : cf.cleaned_data["title"],
                    "url" : cf.cleaned_data["url"],
                    "img" : cf.cleaned_data["img"],
                    "alt" : cf.cleaned_data["alt"],
                    "state" : Status.Close.value,
                    "wtype" : wtype,
                    "time" : timezone.now(),
                    "update_time" : timezone.now(),
                });
                c.save();
                result["requestTips"] = f"Carouse【{c.name}，{c.title}】上传成功，当前处于未启用状态，需手动进行启用。";
                # 发送邮件通知
                try:
                    base_util.sendMsgToAllMgrs(f"Carouse【{c.name}，{c.title}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                except Exception as e:
                    _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
        cid, opType = request.POST.get("cid", None), request.POST.get("opType", None);
        if cid and opType:
            try:
                c = models.Carouse.objects.get(id = cid);
                if opType == "delete":
                    c.delete();
                    result["requestTips"] = f"Carouse【{c.name}，{c.url}，{c.wtype}】成功删除。";
                    # 发送邮件通知
                    try:
                        base_util.sendMsgToAllMgrs(f"Carouse【{c.name}，{c.url}，{c.wtype}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）成功删除。");
                    except Exception as e:
                        _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
            except Exception as e:
                _GG("Log").w(e);
        pass;
    result["form"] = CarouseForm();
    # 返回已发布的轮播图
    infoList = models.Carouse.objects.filter(wtype = wtype).order_by("-update_time");
    result["onlineInfoList"] = [{
        "id" : info.id,
        "name" : info.name,
        "title" : info.title,
        "url" : info.url,
        "img" : info.img.url,
        "alt" : info.alt,
        "time" : info.time,
        "updateTime" : info.update_time,
        "isEnable" : info.state == Status.Open.value and True or False,
    } for info in infoList];
    pass;

# 更新轮播图信息
def update(request, result, wtype = 0):
    cid = request.POST.get("cid", None);
    if cid:
        try:
            c = models.Carouse.objects.get(id = int(cid));
            opType = request.POST.get("opType", "");
            if opType == "enable":
                isEnable = base_util.getPostAsBool(request, "isEnable");
                state = Status.Close.value;
                if isEnable:
                    state = Status.Open.value;
                if c.state != state:
                    c.update_time = timezone.now();
                    c.state = state;
                    c.save();
                result["isSuccess"] = True;
        except Exception as e:
            _GG("Log").w(e);
    pass;
