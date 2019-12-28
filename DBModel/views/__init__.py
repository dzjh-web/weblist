from django.http import JsonResponse;
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
    from game import detail as gameDetail;
    from game import gameLog;
    from release import release;
    from resume import req as resume;
    
except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);


from _Global import _GG;

# 检测Token
def checkToken(func):
    # 获取登陆的用户信息
    def wrapper(request, *args, **kwargs):
        _GG("Log").d("checkToken cookie:", request.COOKIES);
        request.user = None;
        # 根据token信息获取用户信息
        token = _GG("DecodeStr")(request.COOKIES.get("jdreamheart_token", ""));
        if token == _GG("GetReleaseToken")():
            return func(request, *args, **kwargs);
        return JsonResponse({"redult" : "Token异常，请刷新后重试！"});
    return wrapper;