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
	(function(){
		var windowOnresizeFunc = window.onresize; // 响应窗口尺寸大小变化函数
		window.onresize = function(){
			if (windowOnresizeFunc != null) {
				windowOnresizeFunc();
			}
			updateFooterPosition();
		}
		updateFooterPosition();
	})();

	$(".carousel").carousel();
	$("#toTop").on("click",function(){
		$('body,html').animate({scrollTop:0},280);
	});
	// 首页链接
	// var HOME_URL = "http://jimdreamheart.club";
	var HOME_URL = "http://localhost:8000";
	// 登陆链接
	var loginUrl = userInfoUrl + "?k=login";
	// 公钥
	var PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDdTpBdi0thGHpkG1E5F/Imm9FoTtTiSLE1kq+jFuEd0c2K3zpBqrcCOdyQJCy9xc2aMhDUZf0QzGxcMzzcTfGjHv7hXsu5HiKg2Vcm8d35Vq3dZEgJwtkunr0pJtXB64+UniFqepj5zi2elEUwGC5SLeqTjk+ML0YBNBgQEhaSRwIDAQAB-----END PUBLIC KEY-----";
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
	
//	// 定时弹窗
//	if ($('.jumbotron').length > 0) {
//		createIntervalDialog("<h2>定时弹窗</h2><p>测试...</p>", 5);
//	}
})