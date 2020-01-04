from django.http import JsonResponse;
from django.core.cache import cache;
from DBModel import models;

# 加载全局变量
import _load as Loader;
Loader.loadGlobalInfo();


import os,sys;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

try:
    from home import req as home;
    from game import req as game;
    from webkit import req as webkit;
    from release import release;
    from resume import req as resume;
    
except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);


from _Global import _GG;

# 构造user
class User(object):
    is_superuser = False; # 超级用户的标记
    
    # 获取用户名
    def get_username(self):
        return "jdreamheart";

# 检测Token
def checkToken(func):
    # 获取登陆的用户信息
    def wrapper(request, *args, **kwargs):
        _GG("Log").d("checkToken cookie:", request.COOKIES);
        request.user = None;
        # 根据token信息获取用户信息
        token = _GG("DecodeStr")(request.COOKIES.get("jdreamheart_token", ""));
        if cache.has_key(token): # 从缓存中获取token值
            token = cache.get(token);
        if token == _GG("GetReleaseToken")():
            request.user = User();
            return func(request, *args, **kwargs);
        return JsonResponse({"result" : u"Token异常，请刷新后重试！"});
    return wrapper;