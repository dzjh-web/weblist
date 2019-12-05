from django.db.models import Q;
import django.utils.timezone as timezone;
from django.forms import ModelForm;
from ckeditor_uploader.fields import RichTextUploadingFormField;
from django.forms.widgets import HiddenInput;

from DBModel import models;
from utils import base_util;
from release.base import Schedule, sendMsgToAllMgrs;

import json;

from _Global import _GG;

# 游戏日志表单
class GameLogForm(ModelForm):
    class Meta:
        model = models.GameLog
        fields = ["title", "sub_title"]

    def __init__(self, *args, **kwargs):
        super(GameLogForm, self).__init__(*args, **kwargs);
        # 新增内容项
        content = "";
        instance = kwargs.get("instance", None);
        if instance:
            content = instance.cid.content;
        self.fields["content"] = RichTextUploadingFormField(empty_values = content);
        self.files["sketch"] = HiddenInput();

# 上传游戏日志信息
def upload(request, userAuth, result, isSwitchTab):
    if not isSwitchTab:
        gid = request.POST.get("gid", None);
        if gid:
            try:
                gi = models.GameItem.objects.get(id = gid);
                if base_util.getPostAsBool(request, "isRelease"):
                    wf = GameLogForm(request.POST);
                    if wf.is_valid():
                        wc =  models.WebContent(content = wf.cleaned_data["content"]);
                        wc.save();
                        gl = models.GameLog(**{
                            "gid" : gi,
                            "title" : wf.cleaned_data["title"],
                            "sub_title" : wf.cleaned_data["sub_title"],
                            "cid" : wc,
                            "time" : timezone.now(),
                        });
                        gl.save();
                        result["requestTips"] = f"游戏日志【{gl.title}，{gl.sub_title}】上传成功。";
                        # 发送邮件通知
                        try:
                            sendMsgToAllMgrs(f"游戏日志【{gl.title}，{gl.sub_title}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
                else:
                    result["isEdit"] = True;
                    result["form"] = GameLogForm();
                    result["gid"] = gid;
                    return;
            except Exception as e:
                _GG("Log").w(e);
        pass;
    # 返回已发布的游戏
    searchText = request.POST.get("searchText", "");
    infoList = models.GameItem.objects.filter(name__icontains = searchText).order_by('-time');
    result["searchText"] = searchText;
    result["isSearchNone"] = len(infoList) == 0;
    if not searchText:
        result["searchNoneTips"] = f"还未上传过任何游戏网页~";
    else:
        result["searchNoneTips"] = f"未上传过名称包含【{searchText}】的游戏网页，请重新搜索！";
    result["onlineInfoList"] = [{
        "id" : gameInfo.id,
        "name" : gameInfo.name,
        "category" : gameInfo.category,
        "thumbnail" : gameInfo.thumbnail,
        "description" : gameInfo.description,
    } for gameInfo in infoList];
    pass;


# 更新游戏日志信息
def update(request, userAuth, result, isSwitchTab):
    if not isSwitchTab:
        glid = request.POST.get("glid", None);
        if glid:
            try:
                gl = models.GameLog.objects.get(id = glid);
                if base_util.getPostAsBool(request, "isRelease"):
                    wf = GameLogForm(request.POST);
                    if wf.is_valid():
                        gl.cid.content = wf.cleaned_data["content"];
                        gl.cid.save();
                        # 保存游戏日志信息
                        gl.title = wf.cleaned_data["title"];
                        gl.sub_title = wf.cleaned_data["sub_title"];
                        gl.time = timezone.now();
                        gl.save();
                        # 更新成功
                        result["requestTips"] = f"游戏日志【{gl.title}，{gl.sub_title}】更新成功。";
                        # 发送邮件通知
                        try:
                            sendMsgToAllMgrs(f"游戏日志【{gl.title}，{gl.sub_title}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）更新成功。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
                opType = request.POST.get("opType", None);
                if opType:
                    if opType == "update":
                        result["isEdit"] = True;
                        result["form"] = GameLogForm(instance = gl);
                        result["glid"] = glid;
                        return;
                    elif opType == "delete":
                        gl.delete();
                        result["requestTips"] = f"游戏日志【{gl.title}，{gl.sub_title}】成功删除。";
                        # 发送邮件通知
                        try:
                            sendMsgToAllMgrs(f"游戏日志【{gl.title}，{gl.sub_title}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）成功删除。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
            except Exception as e:
                _GG("Log").w(e);
    # 返回已发布的游戏日志
    searchText = request.POST.get("searchText", "");
    infoList = models.GameLog.objects.filter(title__icontains = searchText).order_by('-time');
    result["searchText"] = searchText;
    result["isSearchNone"] = len(infoList) == 0;
    if not searchText:
        result["searchNoneTips"] = f"还未上传过任何游戏日志~";
    else:
        result["searchNoneTips"] = f"未上传过名称包含【{searchText}】的游戏日志，请重新搜索！";
    result["onlineInfoList"] = [{
        "id" : gameInfo.id,
        "title" : gameInfo.title,
        "subTitle" : gameInfo.sub_title,
        "thumbnail" : gameInfo.thumbnail,
        "time" : gameInfo.time,
        "gid" : gameInfo.gid.id,
        "gname" : gameInfo.gid.name,
        "type" : "游戏日志",
    } for gameInfo in infoList];
    pass;
