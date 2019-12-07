import django.utils.timezone as timezone;
from django.forms import ModelForm;

from DBModel import models;
from utils import base_util, random_util;
from release.base import Schedule, sendMsgToAllMgrs;

import hashlib;
import datetime;

from _Global import _GG;

# 简历Token表单
class ResumeTokenForm(ModelForm):
    class Meta:
        model = models.ResumeToken
        fields = ["remarks", "expires"]

# 上传简历Token信息
def upload(request, result, isSwitchTab):
    if not isSwitchTab:
        isRelease = base_util.getPostAsBool(request, "isRelease");
        if isRelease:
            rtf = ResumeTokenForm(request.POST);
            if rtf.is_valid():
                rt = models.ResumeToken(**{
                    "token" : createToken(),
                    "remarks" : rtf.cleaned_data["remarks"],
                    "expires" : rtf.cleaned_data["expires"],
                    "create_at" : timezone.now(),
                    "active_at" : timezone.now(),
                });
                rt.save();
                result["requestTips"] = f"简历Token【{rt.name}，{rt.category}】创建成功。";
                # 发送邮件通知
                try:
                    sendMsgToAllMgrs(f"简历Token【{rt.name}，{rt.category}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                except Exception as e:
                    _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
        pass;
    result["form"] = ResumeTokenForm();
    pass;

# 创建Token
def createToken():
    randCode = random_util.randomMulti(32); # 32位随机码
    return hashlib.md5("|".join([timezone.now(), randCode]).encode("utf-8")).hexdigest();

# 获取已创建的Token
def getOlTokenList():
    infoList = models.ResumeToken.objects.all().order_by('-active_at');
    olList = [];
    for info in infoList:
        olInfo = {
            "id" : info.id,
            "token" : info.token,
            "remarks" : info.remarks,
            "expires" : info.expires,
            "create_at" : info.create_at,
            "active_at" : info.active_at,
            "state" : "已过期",
            "isNotActive" : True,
        };
        if info.expires > 0:
            targetTime = info.active_at + datetime.timedelta(days = info.expires);
            delta = targetTime - datetime.datetime.now();
            leftDays = datetime.days() + datetime.seconds() / 86400;
            if leftDays > 0:
                olInfo["state"] = f"剩余{leftDays}天";
                olInfo["isNotActive"] = False;
        olList.append(olInfo);
    result["onlineInfoList"] = olList;