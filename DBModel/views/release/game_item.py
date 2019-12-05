from django.db.models import Q;
import django.utils.timezone as timezone;
from django.forms import ModelForm;
from ckeditor_uploader.fields import RichTextUploadingFormField;

from DBModel import models;
from utils import base_util;
from release.base import Schedule, sendMsgToAllMgrs;

import json;

from _Global import _GG;

# 游戏网页表单
class GameItemForm(ModelForm):
    class Meta:
        model = models.GameItem
        fields = ["name", "category", "thumbnail", "description", "file_path"]

    def __init__(self, *args, **kwargs):
        super(GameItemForm, self).__init__(*args, **kwargs);
        # 新增内容项
        content = "";
        instance = kwargs.get("instance", None);
        if instance:
            content = instance.cid.content;
        self.fields["content"] = RichTextUploadingFormField(empty_values = content);

# 上传游戏网页信息
def upload(request, userAuth, result, isSwitchTab):
    if not isSwitchTab:
        isRelease = base_util.getPostAsBool(request, "isRelease");
        if isRelease:
            wf = GameItemForm(request.POST);
            if wf.is_valid():
                wc =  models.WebContent(content = wf.cleaned_data["content"]);
                wc.save();
                gi = models.GameItem(**{
                    "name" : wf.cleaned_data["name"],
                    "category" : wf.cleaned_data["category"],
                    "thumbnail" : wf.cleaned_data["thumbnail"],
                    "description" : wf.cleaned_data["description"],
                    "cid" : wc,
                    "schedule" : Schedule.Pending.value,
                    "time" : timezone.now(),
                });
                gi.save();
                result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】上传成功。";
                # 发送邮件通知
                try:
                    sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                except Exception as e:
                    _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
        pass;
    result["form"] = GameItemForm();
    pass;


# 更新游戏网页信息
def update(request, userAuth, result, isSwitchTab):
    if not isSwitchTab:
        gid = request.POST.get("gid", None);
        if gid:
            try:
                gi = models.GameItem.objects.get(id = gid);
                if "schedule" in request.POST:
                    # 更新进度值
                    gi.schedule = request.POST["schedule"];
                    gi.save();
                if base_util.getPostAsBool(request, "isRelease"):
                    wf = GameItemForm(request.POST);
                    if wf.is_valid():
                        gi.cid.content = wf.cleaned_data["content"];
                        gi.cid.save();
                        # 保存游戏网页信息
                        gi.name = wf.cleaned_data["name"];
                        gi.category = wf.cleaned_data["category"];
                        gi.thumbnail = wf.cleaned_data["thumbnail"];
                        gi.description = wf.cleaned_data["description"];
                        gi.time = timezone.now();
                        gi.save();
                        # 更新成功
                        result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】更新成功。";
                        # 发送邮件通知
                        try:
                            sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）更新成功。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
                opType = request.POST.get("opType", None);
                if opType:
                    if opType == "update":
                        result["isEdit"] = True;
                        result["form"] = GameItemForm(instance = gi);
                        result["gid"] = gid;
                        return;
                    elif opType == "delete":
                        # 删除游戏日志
                        for log in models.GameLog.objects.filter(gid = gi):
                            log.delete();
                        # 删除游戏网页
                        gi.delete();
                        result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】成功删除。";
                        # 发送邮件通知
                        try:
                            sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）成功删除。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
            except Exception as e:
                _GG("Log").w(e);
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
        "schedule" : gameInfo.schedule,
        "filePath" : gameInfo.file_path and gameInfo.file_path.url or "",
        "time" : gameInfo.time,
        "type" : "游戏网页",
    } for gameInfo in infoList];
    pass;
