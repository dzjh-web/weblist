from django.db.models import Q;
import django.utils.timezone as timezone;
from django.forms import ModelForm;
from ckeditor_uploader.fields import RichTextUploadingFormField;

from DBModel import models;
from utils import base_util;
from release.base import Schedule, ScheduleMap;

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
        self.fields["content"] = RichTextUploadingFormField(label = "详细内容", initial = content);

# 上传游戏网页信息
def upload(request, result, isSwitchTab):
    if not isSwitchTab:
        isRelease = base_util.getPostAsBool(request, "isRelease");
        if isRelease:
            wf = GameItemForm(request.POST, request.FILES);
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
                    "update_time" : timezone.now(),
                    "sort_id" : 0,
                });
                gi.save();
                result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】上传成功。";
                # 发送邮件通知
                try:
                    base_util.sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                except Exception as e:
                    _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
        pass;
    result["form"] = GameItemForm();
    pass;


# 更新游戏网页信息
def update(request, result, isSwitchTab):
    if not isSwitchTab:
        gid = request.POST.get("gid", None);
        if gid:
            try:
                isEdit = False;
                gi = models.GameItem.objects.get(id = int(gid));
                if base_util.getPostAsBool(request, "isRelease"):
                    wf = GameItemForm(request.POST, request.FILES);
                    if wf.is_valid():
                        gi.cid.content = wf.cleaned_data["content"];
                        gi.cid.save();
                        # 保存游戏网页信息
                        gi.name = wf.cleaned_data["name"];
                        gi.category = wf.cleaned_data["category"];
                        if wf.cleaned_data["thumbnail"]:
                            gi.thumbnail = wf.cleaned_data["thumbnail"];
                        if wf.cleaned_data["file_path"]:
                            gi.file_path = wf.cleaned_data["file_path"];
                        gi.description = wf.cleaned_data["description"];
                        gi.update_time = timezone.now();
                        gi.save();
                        # 更新成功
                        result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】更新成功。";
                        # 跳转编辑页面
                        isEdit = True;
                        # 发送邮件通知
                        try:
                            base_util.sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）更新成功。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
                    else:
                        _GG("Log").w(f"Invalid form data!");
                opType = request.POST.get("opType", None);
                if opType:
                    if opType == "update":
                        # 更新进度值
                        if "schedule" in request.POST:
                            gi.schedule = request.POST["schedule"];
                            gi.update_time = timezone.now();
                            gi.save();
                            result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】排序值（{gi.schedule}）更新成功。";
                        # 更新排序值
                        if "sortId" in request.POST:
                            gi.sort_id = int(request.POST["sortId"]);
                            gi.update_time = timezone.now();
                            gi.save();
                            result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】排序值（{gi.sort_id}）更新成功。";
                        # 跳转编辑页面
                        isEdit = True;
                    elif opType == "delete":
                        # 删除游戏日志
                        for log in models.GameLog.objects.filter(gid = gi):
                            log.delete();
                        # 删除游戏网页
                        gi.delete();
                        result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】成功删除。";
                        # 发送邮件通知
                        try:
                            base_util.sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）成功删除。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
                # 返回页面数据
                if isEdit:
                    result["isEdit"] = True;
                    result["form"] = GameItemForm(instance = gi);
                    result["gid"] = gid;
                    # 进度
                    result["schedule"] = ScheduleMap.get(gi.schedule, "未知");
                    result["scheduleInfoList"] = [{"key" : v, "val" : k} for k,v in ScheduleMap.items()];
                    # 排序值
                    result["sortId"] = gi.sort_id;
                    return;
            except Exception as e:
                _GG("Log").w(e);
    # 返回已发布的游戏
    searchText = request.POST.get("searchText", "");
    infoList = models.GameItem.objects.filter(name__icontains = searchText).order_by("-sort_id", "-update_time");
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
        "thumbnail" : gameInfo.thumbnail.url,
        "description" : gameInfo.description,
        "schedule" : ScheduleMap.get(gameInfo.schedule, "未知"),
        "filePath" : gameInfo.file_path and gameInfo.file_path.url or "",
        "time" : gameInfo.time,
        "updateTime" : gameInfo.update_time,
        "sortId" : gameInfo.sort_id,
        "type" : "游戏网页",
    } for gameInfo in infoList];
    pass;
