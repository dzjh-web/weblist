# -*- coding: utf-8 -*-
# @Author: JDreamHeart
# @Date:   2018-04-19 14:22:56
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-11 13:32:12
import re,os,sys,time;
import hashlib;
import datetime;
import json;
from utils import random_util;

logLevel = "debug";

# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
# 添加搜索路径
if CURRENT_PATH not in sys.path:
	sys.path.append(CURRENT_PATH);
if os.path.join(CURRENT_PATH, "core") not in sys.path:
	sys.path.append(os.path.join(CURRENT_PATH, "core"));

# 加载全局变量
import _Global as _G;
from logCore.Logger import Logger;
from rsaCore import encodeStr, decodeStr, getPublicKey;
from utils import base_util;

from weblist.settings import HOME_URL;

# 初始化全局变量
def _initGlobal_G_():
	_G.initGlobal_GTo_Global();

# 锁定全局变量
def _lockGlobal_G_():
	_G.lockGlobal_GTo_Global();

# 加载全局变量信息
def loadGlobalInfo():
	_initGlobal_G_(); # 初始化全局变量
	_loadGlobal_(); # 加载全局变量
	_lockGlobal_G_(); # 锁定全局变量

# 加载全局变量
def _loadGlobal_():
	_loadPaths_(); # 加载全局路径名变量
	_loadLogger_(); # 加载日志类变量
	_loadRsaDecode_(); # 加载rsa密钥解码方法
	_loadReleaseToken_(); # 加载发布token

# 加载全局路径名变量
def _loadPaths_():
	_G.setGlobalVarTo_Global("ProjectPath", CURRENT_PATH + "/");
	pass;

# 加载全局日志类
def _loadLogger_():
	# Logger参数
	path = "log";
	name = "dzjh-weblist";
	curTimeStr = time.strftime("%Y_%m_%d", time.localtime());
	maxBytes = 102400000;
	backupCount = 10;
	# 保存Logger到全局变量中
	logger = Logger("Common", level = logLevel, isLogFile = True, logFileName = os.path.join(CURRENT_PATH, path, name+("_%s.log"%curTimeStr)), maxBytes = maxBytes, backupCount = backupCount);
	_G.setGlobalVarTo_Global("Log", logger); # 设置日志类的全局变量
	return logger;

# 加载rsa密钥解码方法
def _loadRsaDecode_():
	# 加载rsa密钥编解码方法
	_G.setGlobalVarTo_Global("EncodeStr", encodeStr);
	_G.setGlobalVarTo_Global("DecodeStr", decodeStr);
	# 更新main.js的公钥和首页地址
	publicKey = getPublicKey();
	publicKey = publicKey.replace("\n", "")
	mainJSFile, content = os.path.join(CURRENT_PATH, "assets", "static", "js", "main.js"), "";
	with open(mainJSFile, "r", encoding = "utf-8") as f:
		isPking = False;
		for line in f.readlines():
			# 更新HOME_URL
			if re.search("var HOME_URL.*=.*\".*\"", line):
				line = re.sub("\".*\";?", f"\"{HOME_URL}\";", line);
			# 更新PUBLIC_KEY
			if re.search("var PUBLIC_KEY.*\".*\"", line):
				line = re.sub("\".*\";?", f"\"{publicKey}\";", line);
			elif re.search("var PUBLIC_KEY.*\".*", line):
				line = re.sub("\".*;?", f"\"{publicKey}\";", line);
				isPking = True;
			else:
				if isPking:
					if re.search("\";?", line):
						isPking = False;
					continue;
			content += line;
	with open(mainJSFile, "w", encoding = "utf-8") as f:
		f.write(content);

# 加载发布Token
def _loadReleaseToken_():
	tokenFilePath = os.path.join(CURRENT_PATH, "release_token.json");
	# 设置获取发布Token的全局方法
	global lastReleaseTokenTime;
	global releaseToken;
	releaseToken = ""; # 初始化
	# 更新Token
	def updateToken():
		# 更新时间
		global lastReleaseTokenTime;
		lastReleaseTokenTime = datetime.datetime.now();
		# 生成Token
		global releaseToken;
		randCode = random_util.randomMulti(32); # 32位随机码
		releaseToken = hashlib.md5("|".join([datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"), randCode]).encode("utf-8")).hexdigest();
		_G._GG("Log").i("======== New Release Token ========", releaseToken);
		base_util.sendMsgToAllMgrs(f"JDreamHeart New Release Token: {releaseToken}.");
		# 保存到文件中
		with open(tokenFilePath, "w") as f:
			f.write(json.dumps({
				"token" : releaseToken,
				"timestamp" : lastReleaseTokenTime.timestamp(),
			}));
	# 获取Token
	def getToken():
		global lastReleaseTokenTime;
		delta = datetime.datetime.now() - lastReleaseTokenTime;
		if delta.days >= 10:
			updateToken(); # 距离上次请求超过10天，更新Token
		global releaseToken;
		return releaseToken;
	# 设置获取Token的全局变量
	_G.setGlobalVarTo_Global("GetReleaseToken", getToken);
	# 检测更新当前Token
	if os.path.exists(tokenFilePath):
		with open(tokenFilePath, "r") as f:
			info = json.loads(f.read());
			if "token" in info and "timestamp" in info:
				releaseToken = info["token"];
				lastReleaseTokenTime = datetime.datetime.fromtimestamp(info["timestamp"]);
		pass;
	# 判断是否更新Token
	if not releaseToken:
		updateToken();
