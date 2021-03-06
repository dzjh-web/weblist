from django.db.models import Q;
import django.utils.timezone as timezone;
from django.forms import ModelForm;
from ckeditor_uploader.fields import RichTextUploadingFormField;

from weblist.settings import HOME_URL;

from DBModel import models;
from utils import base_util, random_util;
from release.base import Schedule, ScheduleMap, Status;

import json;

from _Global import _GG;


# 游戏网页表单
class GameItemForm(ModelForm):
    class Meta:
        model = models.GameItem
        fields = ["name", "category", "thumbnail", "description", "version", "file_path", "demo_video"]

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
                    "state" : Status.Close.value,
                    "token" : random_util.randomToken(),
                });
                gi.save();
                result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】上传成功。";
                # 发送邮件通知
                try:
                    base_util.sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                except Exception as e:
                    _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
            else:
                result["requestFailedTips"] = f"游戏网页内容无效！";
                _GG("Log").w(f"Invalid game web!");
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
                        if wf.cleaned_data["version"]:
                            gi.version = wf.cleaned_data["version"];
                        if wf.cleaned_data["file_path"]:
                            gi.file_path = wf.cleaned_data["file_path"];
                        if wf.cleaned_data["demo_video"]:
                            gi.demo_video = wf.cleaned_data["demo_video"];
                        gi.description = wf.cleaned_data["description"];
                        gi.update_time = timezone.now();
                        gi.save();
                        # 更新成功
                        result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】更新成功。";
                        # 跳转编辑页面
                        isEdit = True;
                        # 发送邮件通知
                        try:
                            base_util.sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')}）更新成功。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
                    else:
                        result["requestFailedTips"] = f"游戏网页内容无效！";
                        _GG("Log").w("Invalid form data!");
                opType = request.POST.get("opType", None);
                if opType:
                    if opType == "update":
                        # 更新进度值
                        if "schedule" in request.POST:
                            gi.schedule = request.POST["schedule"];
                            gi.update_time = timezone.now();
                            gi.save();
                            result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】进度（{gi.schedule}）更新成功。";
                        # 更新排序值
                        if "sortId" in request.POST:
                            gi.sort_id = int(request.POST["sortId"]);
                            gi.update_time = timezone.now();
                            gi.save();
                            result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】排序值（{gi.sort_id}）更新成功。";
                        # 更新状态
                        if "state" in request.POST:
                            if request.POST["state"] == "open":
                                gi.state = Status.Open.value;
                            else:
                                gi.state = Status.Close.value;
                            gi.update_time = timezone.now();
                            gi.save();
                            result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】状态更新成功。";
                        # 更新Token
                        if "token" in request.POST:
                            gi.token = random_util.randomToken();
                            gi.update_time = timezone.now();
                            gi.save();
                            result["requestTips"] = f"游戏网页【{gi.name}，{gi.category}】Token值（{gi.token}）更新成功。";
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
                            base_util.sendMsgToAllMgrs(f"游戏网页【{gi.name}，{gi.category}】于（{timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')}）成功删除。");
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
                    # 状态信息
                    result["stateInfo"] = {"state" : "close", "label" : "关闭", "style" : "danger"};
                    if gi.state == Status.Close.value:
                        result["stateInfo"] = {"state" : "open", "label" : "启用", "style" : "primary"};
                    # Token值
                    result["token"] = gi.token;
                    result["token_url"] = f"{HOME_URL}/game?k=detail&gid={gi.id}&token={gi.token}";
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
        "version" : gameInfo.version or "0.0",
        "filePath" : gameInfo.file_path and gameInfo.file_path.url or "",
        "demoVideo" : gameInfo.demo_video,
        "time" : gameInfo.time,
        "updateTime" : gameInfo.update_time,
        "sortId" : gameInfo.sort_id,
        "state" : gameInfo.state == Status.Open.value and "启用" or "关闭",
        "type" : "游戏网页",
    } for gameInfo in infoList];
    pass;
