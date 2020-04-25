import django.utils.timezone as timezone;
from django.forms import ModelForm;

from DBModel import models;
from utils import base_util, random_util;
from release.base import Schedule;

import datetime;

from _Global import _GG;

# 简历Token表单
class ResumeTokenForm(ModelForm):
    class Meta:
        model = models.ResumeToken
        fields = ["name", "remarks", "expires"]

# 上传简历Token信息
def upload(request, result, isSwitchTab):
    if not isSwitchTab:
        isRelease = base_util.getPostAsBool(request, "isRelease");
        if isRelease:
            rtf = ResumeTokenForm(request.POST, request.FILES);
            if rtf.is_valid():
                rt = models.ResumeToken(**{
                    "token" : createToken(),
                    "name" : rtf.cleaned_data["name"],
                    "remarks" : rtf.cleaned_data["remarks"],
                    "expires" : rtf.cleaned_data["expires"],
                    "create_at" : timezone.now(),
                    "active_at" : timezone.now(),
                });
                rt.save();
                result["requestTips"] = f"简历Token【{rt.token}】创建成功。";
                # 发送邮件通知
                try:
                    base_util.sendMsgToAllMgrs(f"简历Token【{rt.token}】于（{timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                except Exception as e:
                    _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
            else:
                result["requestFailedTips"] = "简历信息无效！";
                _GG("Log").w("Invalid resume info!");
        else:
            opType = request.POST.get("opType", "");
            if opType:
                try:
                    tid = request.POST.get("tid", -1);
                    t = models.ResumeToken.objects.get(id = int(tid));
                    if opType == "change_remarks":
                        if "remarks" in request.POST:
                            t.remarks = request.POST["remarks"];
                            t.save();
                    elif opType == "change_expires":
                        if "expires" in request.POST:
                            t.expires = int(request.POST["expires"]);
                            t.save();
                    elif opType == "active":
                        t.active_at = timezone.now();
                        t.save();
                    elif opType == "delete":
                        t.delete();
                except Exception as e:
                    _GG("Log").e(f"Failed to operate resume token! Err[{e}]!");
    result["form"] = ResumeTokenForm();
    result["onlineInfoList"] = getOlTokenList();
    pass;

# 创建Token
def createToken():
    return random_util.randomToken(); # 随机Token

# 获取已创建的Token
def getOlTokenList():
    infoList = models.ResumeToken.objects.all().order_by('-active_at');
    olList = [];
    for info in infoList:
        olInfo = {
            "id" : info.id,
            "token" : info.token,
            "name" : info.name or "",
            "remarks" : info.remarks or "",
            "expires" : info.expires,
            "create_at" : info.create_at,
            "active_at" : info.active_at,
            "state" : "已过期",
            "isNotActive" : True,
        };
        if info.expires > 0:
            targetTime = info.active_at + datetime.timedelta(days = info.expires);
            delta = targetTime - timezone.now();
            leftDays = delta.days + delta.seconds / 86400;
            if leftDays > 0:
                olInfo["state"] = "剩余{:.2f}天".format(leftDays);
                olInfo["isNotActive"] = False;
        olList.append(olInfo);
    return olList;