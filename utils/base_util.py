from django.core.mail import send_mail
from weblist.settings import EMAIL_HOST_USER

from _Global import _GG;

# 获取post数据的bool类型
def getPostAsBool(request, key):
    return request.POST.get(key, "") == "true";

# 发送消息给所有管理员
def sendMsgToAllMgrs(msg):
    mgrEmails = ["15602291936@163.com"];
    return sendToEmails(msg, mgrEmails);

def sendToEmails(msg, emails):
    # 发送邮件给指定邮箱
    try:
        send_mail("JDreamHeart通知", msg, EMAIL_HOST_USER, emails, fail_silently=False);
        return True;
    except Exception as e:
        _GG("Log").e("邮件发送失败!", e);
    return False;