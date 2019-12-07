$(function(){
	// 更新footer的位置
	updateFooterPosition = function() {
		if ($(window).height() > $("body").height()) {
			$("footer").css({position:"fixed", bottom:0});
		} else {
			$("footer").css({position:"static", bottom:0});
		}
	};
	// 监听窗口尺寸大小变化
	var resizeCallbackList = [updateFooterPosition];
	(function(){
		var windowOnresizeFunc = window.onresize; // 响应窗口尺寸大小变化函数
		window.onresize = function(){
			if (windowOnresizeFunc != null) {
				windowOnresizeFunc();
			}
			resizeCallbackList.forEach(function(callback) {
				callback();
			})
		}
		updateFooterPosition();
	})();

	$(".carousel").carousel();
	$("#toTop").on("click",function(){
		$('body,html').animate({scrollTop:0},280);
	});
	// 首页链接
	// var HOME_URL = "http://jimdreamheart.club";
	var HOME_URL = "http://localhost:8008";
	// 登陆链接
	var loginUrl = HOME_URL + "/release";
	// 公钥
	var PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDRaMBbz374GyG4r1xl8b7495tzQQo06XXNB6LZEO8SasL+1oxtmB5RYDKIdx4I1oEohoYGiwNrnpVoxAl/yS/gnK/n1EI3QfI0NhuPSQBH+cbjOK7VbX/LDLeNvGayTxzRWYvpTJbREQ2lo0XySJwgBuGLWU4/GDxKjT0XxXsNRwIDAQAB-----END PUBLIC KEY-----";
	// 编码字符串
	encodeStr = function(s) {
		var ec = new JSEncrypt();
		ec.setPublicKey(PUBLIC_KEY);
		return ec.encrypt(s);
	}
	// 获取提示文档
	var getAlertTips = function(type, tips) {
		return "<div class='alert alert-"+ type +"' role='alert'>\
			<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>\
			<span class='alertContent'>"+ tips +"</span>\
		</div>";
	}
	// 登陆平台
    loginIP = function(formId, callback){
		var token = $("#"+formId+" input[name='token']").val();
		$.post(loginUrl, {
			isLogin : true,
			token : encodeStr(token),
		}, function(data, status){
			if (status == "success") {
				if (!data.isSuccess) {
					$("#"+formId).prepend(getAlertTips("danger", data.tips));
					return;
				}
				console.log("登陆成功。");
				// 登陆成功回调
				callback();
			} else {
				alert("登陆失败！")
			}
		});
    }
	// 登出平台
    logoutIP = function(formId, callback){
		$.post(loginUrl, {
			isLogout : true,
		}, function(data, status){
			if (status == "success") {
				if (!data.isSuccess) {
					if (formId != null) {
						$("#"+formId).prepend(getAlertTips("danger", data.tips));
					}
					return;
				}
				console.log("登出成功。");
				// 登出成功回调
				callback();
			} else {
				alert("登出失败！")
			}
		});
    }
	// 关闭弹窗
	closeDialogPage = function(){
		if ($('#dialogPage').length > 0) 	{
			$('#dialogPage').remove();
		}
	}
	// 创建弹窗函数[带有关闭回调参数]
	createDialog = function(content, closeCallback){
		// 关闭原有弹窗
		closeDialogPage();
		// 弹窗内容
		var dialogPage = "<div id='dialogPage'>\
			<div class='container'>\
				<div class='row'>\
					<div class='dialog-background col-md-4 col-md-offset-4'>\
						<a id='closeDialogPage' href='javascript:void(0);' title='关闭弹窗'><span class='glyphicon glyphicon-remove'></span>关闭</a>\
						<div class='dialog-content'>" + content + "</div>\
					</div>\
				</div>\
			</div>\
		</div>";
		// 添加弹窗
		$("body").append(dialogPage);
		// 更新弹窗页尺寸方法
		function updateDialogPageSize(){
			if ($('#dialogPage').length > 0) {
				var pageWidth = Math.max($(window).width(), $("body").width());
				$('#dialogPage').width(pageWidth);
				var pageHeight = Math.max($(window).height(), $("body").height());
				$('#dialogPage').height(pageHeight);
				// 移动到弹窗中心
				$('body,html').animate({scrollLeft : (pageWidth - $(window).width())/2, scrollTop: (pageHeight - $(window).height())/2}, 0);
			}
		}
		updateDialogPageSize();
		// 监听窗口尺寸变化方法
		var windowOnresizeFunc = window.onresize;
		window.onresize = function(){
			if (windowOnresizeFunc != null) {
				windowOnresizeFunc();
			}
			updateDialogPageSize();
		}
		// 点击关闭的事件
		$("#closeDialogPage").on("click",function(){
			// 移除弹窗页
			closeDialogPage();
			// 重置窗口大小事件
			window.onresize = windowOnresizeFunc;
			// 回调关闭函数
			closeCallback();
		});
	}
	// 创建弹窗函数
	createDialogPage = function(content){
		createDialog(content, function(){}); // 关闭弹窗时无回调
	}
	// 创建定时弹窗
	createIntervalDialog = function(content, seconds, closeCallback){
		// 设置定时器
		var intervalId = window.setInterval(function(){
			seconds--
			if (seconds < 0) {
				window.clearInterval(intervalId);
				//关闭弹窗
				closeDialogPage();
			}
			if ($('#timeCountDown').length > 0) {
				$('#timeCountDown').html(seconds);
			}
		}, 1000);
		// 创建弹窗
		createDialog("<div class='text-center'>"+ content +"<p class='dialog-interval'><span id='timeCountDown'>"+ seconds +"</span>&nbsp;秒后自动关闭</p></div>", function(){
			window.clearInterval(intervalId);
			closeCallback();
		});
	}
    // 添加input到form中
    var addInputToForm = function(item, name, value, type){
        var $input = item.find("input[name='" + name + "']");
        if ($input.length > 0) {
            $input.val(value);
            if ($input.attr("type") != type) {
                $input.attr("type", type)
            }
        } else {
            item.append("<input name='" + name + "' class='hidden' type='" + type + "' value='" + value + "' />");
        }
    }
    // 添加数据到表单
    addInputsToForm = function(item, exIpts){
        // 添加扩展输入
        if (exIpts instanceof Array && exIpts.length > 0) {
            for (var i = 0; i < exIpts.length; i++) {
                var ipt = exIpts[i];
                addInputToForm(item, ipt.key, ipt.val, ipt.type);
            }
        }
	}
	// 翻转卡片构造函数
	FlipCardIndex = function(node) {
		this.node = node;
		this.defaultClassName = "";
		this.init();
	};
	FlipCardIndex.prototype.init = function () {
		var self = this;
		Array.prototype.slice.call(self.node, 0).forEach(function (item, _) {
			self.updateItem(item);
			self.bindEvents(item);
			resizeCallbackList.push(function(){
				if (self.node.length > 0) {
					self.updateItem(item);
				}
			});
		});
	};
	FlipCardIndex.prototype.updateItem = function (item) {
		let w = this.rect(item).w;
		$(item).height(w);
		$(item).find(".card-info").css("transform-origin", "50% 50% -" + w/2 + "px");
		$(item).find(".card-content").css("height", w + "px");
	};
	FlipCardIndex.prototype.rect = function (item) {
		var offset = $(item).offset();
		return {
			w: $(item).width(),
			h: $(item).height(),
			l: offset.left,
			t: offset.top,
		}
	};
	FlipCardIndex.prototype.bindEvents = function (item) {
		var self = this;
		$(item).on("mouseenter", function (e) {
			self.addClass(e, item, "in");
			return false;
			
		})
		$(item).on("mouseleave", function (e) {
			self.addClass(e, item, "out");
			return false;
		})
	};
	FlipCardIndex.prototype.setDefaultClassName = function (className) {
		this.defaultClassName = className;
	};
	FlipCardIndex.prototype.addClass = function (e, item, state) {
		var direction = this.getDirection(e, item);
		var class_suffix = "";
		switch (direction) {
			case 0:
				class_suffix = "-top"; 
				break;
			case 1:
				class_suffix = "-right"; 
				break;
			case 2:
				class_suffix = "-bottom";
				break;
			case 3:
				class_suffix = "-left"; 
				break;
		}
		item.className = this.defaultClassName;
		item.classList.add(state + class_suffix);
	};
	FlipCardIndex.prototype.getDirection = function (e, item) {
		var self = this;
		var curNodeRect = self.rect(item);
		var w = curNodeRect.w,
			h = curNodeRect.h,
			x = e.pageX - curNodeRect.l - w / 2,
			y = e.pageY - curNodeRect.t - h / 2;
		return (Math.round(((Math.atan2(y, x) * (180 / Math.PI)) + 180) / 90)+3) % 4;
	};

//	// 定时弹窗
//	if ($('.jumbotron').length > 0) {
//		createIntervalDialog("<h2>定时弹窗</h2><p>测试...</p>", 5);
//	}
})