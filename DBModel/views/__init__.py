from DBModel import models;

from _Global import _GG;

import os,sys;

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
sys.path.append(CURRENT_PATH);

try:
    from home import req as home;
    from game import req as game;
    
except Exception as e:
	raise e;
finally:
	sys.path.remove(CURRENT_PATH);


# 检测Token
def checkToken(func):
    # 获取登陆的用户信息
    def wrapper(request, *args, **kwargs):
        _GG("Log").d("checkToken cookie:", request.COOKIES);
        request.user = None;
        # 根据token信息获取用户信息
        token = _GG("DecodeStr")(request.COOKIES.get("weblist_token", ""));
        if token:
            try:
                request.user = models.ReleaseAuthority.objects.get(token = token);
            except Exception as e:
                _GG("Log").w(e);
        return func(request, *args, **kwargs);
    return wrapper;