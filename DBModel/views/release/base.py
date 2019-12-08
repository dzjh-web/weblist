
from enum import Enum;

# 网页类型穷举值
class WebType(Enum):
    Unknown = 0 # 未知网页
    Home    = 1 # 首页网页
    Github  = 2 # Github网页
    Wiki    = 3 # 文档网页
    Game    = 4 # 游戏网页

# 网页状态穷举值
class Status(Enum):
    Close   = 0 # 关闭
    Open    = 1 # 启用
    Off     = 2 # 下架

# 进度穷举值
class Schedule(Enum):
    Pending = 0 # 挂起
    Plan    = 1 # 计划中
    Prepare = 2 # 筹备中
    Develop = 3 # 开发中
    Test    = 4 # 测试中
    Release = 5 # 已发布
    Off     = 6 # 已下架
