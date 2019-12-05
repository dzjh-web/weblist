from django.db.models import Q;
import django.utils.timezone as timezone;
from django.forms import ModelForm;
from ckeditor_uploader.fields import RichTextUploadingFormField;

from DBModel import models;
from utils import base_util;
from release.base import WebType, Status, sendMsgToAllMgrs;

import json;

from _Global import _GG;

webTypeTitleMap = {
    WebType.Home.value : "首页网页",
    WebType.Github.value : "Github网页",
    WebType.Wiki.value : "文档网页",
};

# 网页表单
class WebItemForm(ModelForm):
    class Meta:
        model = models.WebItem
        fields = ["name", "title", "thumbnail", "description", "url"]

    def __init__(self, *args, **kwargs):
        super(WebItemForm, self).__init__(*args, **kwargs);
        # 新增内容项
        content = "";
        instance = kwargs.get("instance", None);
        if instance:
            content = instance.cid.content;
        self.fields["content"] = RichTextUploadingFormField(empty_values = content);

# 上传首页的网页信息
def upload(request, userAuth, result, isSwitchTab, wtype = 0):
    result["title"] = webTypeTitleMap.get(wtype, "网页");
    if not isSwitchTab:
        isRelease = base_util.getPostAsBool(request, "isRelease");
        if isRelease:
            wf = WebItemForm(request.POST);
            if wf.is_valid():
                wc =  models.WebContent(content = wf.cleaned_data["content"]);
                wc.save();
                wi = models.WebItem(**{
                    "name" : wf.cleaned_data["name"],
                    "title" : wf.cleaned_data["title"],
                    "thumbnail" : wf.cleaned_data["thumbnail"],
                    "description" : wf.cleaned_data["description"],
                    "url" : wf.cleaned_data["url"],
                    "cid" : wc,
                    "wtype" : wtype,
                    "state" : Status.Close.value,
                    "time" : timezone.now(),
                });
                wi.save();
                result["requestTips"] = f"网页【{wi.name}，{wi.title}】上传成功，当前处于关闭状态，需手动进行启用。";
                # 发送邮件通知
                try:
                    sendMsgToAllMgrs(f"网页【{wi.name}，{wi.title}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）上传成功。");
                except Exception as e:
                    _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
        pass;
    result["form"] = WebItemForm();
    pass;


# 更新首页的网页信息
def update(request, userAuth, result, isSwitchTab, wtype = 0):
    result["title"] = webTypeTitleMap.get(wtype, "网页");
    if not isSwitchTab:
        wid = request.POST.get("wid", None);
        if wid:
            try:
                wi = models.WebItem.objects.get(id = wid);
                if "state" in request.POST:
                    if request.POST["state"] == "open":
                        wi.state = Status.Close.value;
                    else:
                        wi.state = Status.Open.value;
                    wi.save();
                if base_util.getPostAsBool(request, "isRelease"):
                    wf = WebItemForm(request.POST);
                    if wf.is_valid():
                        wi.cid.content = wf.cleaned_data["content"];
                        wi.cid.save();
                        # 保存网页信息
                        wi.name = wf.cleaned_data["name"];
                        wi.title = wf.cleaned_data["title"];
                        wi.thumbnail = wf.cleaned_data["thumbnail"];
                        wi.description = wf.cleaned_data["description"];
                        wi.url = wf.cleaned_data["url"];
                        wi.time = timezone.now();
                        wi.save();
                        # 更新成功
                        result["requestTips"] = f"网页【{wi.name}，{wi.title}】更新成功。";
                        # 发送邮件通知
                        try:
                            sendMsgToAllMgrs(f"网页【{wi.name}，{wi.title}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）更新成功。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
                opType = request.POST.get("opType", None);
                if opType:
                    if opType == "update":
                        result["isEdit"] = True;
                        result["form"] = WebItemForm(instance = wi);
                        result["wid"] = wid;
                        return;
                    elif opType == "delete":
                        wi.delete();
                        result["requestTips"] = f"网页【{wi.name}，{wi.title}】成功删除。";
                        # 发送邮件通知
                        try:
                            sendMsgToAllMgrs(f"网页【{wi.name}，{wi.title}】于（{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}）成功删除。");
                        except Exception as e:
                            _GG("Log").e(f"Failed to send message to all managers! Error({e})!");
            except Exception as e:
                _GG("Log").w(e);
    # 返回已发布的网页
    searchText = request.POST.get("searchText", "");
    infoList = models.WebItem.objects.filter(Q(name__icontains = searchText) | Q(title__icontains = searchText), wtype = wtype).order_by('-time');
    result["searchText"] = searchText;
    result["isSearchNone"] = len(infoList) == 0;
    if not searchText:
        result["searchNoneTips"] = f"还未上传过任何网页~";
    else:
        result["searchNoneTips"] = f"未上传过名称（或标题）包含【{searchText}】的网页，请重新搜索！";
    result["onlineInfoList"] = [{
        "id" : webInfo.id,
        "name" : webInfo.name,
        "title" : webInfo.title,
        "thumbnail" : webInfo.thumbnail,
        "description" : webInfo.description,
        "url" : webInfo.url,
        "time" : webInfo.time,
        "type" : "首页网页",
    } for webInfo in infoList];
    pass;
