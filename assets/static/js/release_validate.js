$(function(){
    // 校验版本
    $.validator.addMethod(
        "checkVersion",
        function(value, element, param){
            if (this.optional(element)) {
                return false;
            }
            var verList = value.split(".");
            if (verList.length != param) {
                return false;
            }
            var ret = true;
            verList.forEach(function(item){
                ret = /^\d+$/.test(item)
            });
            return ret;
        },
        "请输入正确的版本格式（如，1.0.0）"
    );
    // 校验文件类型
    $.validator.addMethod(
        "checkFileType",
        function(value, element, param){
            if (this.optional(element)) {// 允许文件为空
                return true;
            }
            var valList = value.split(".");
            var val = valList[valList.length-1];
            if (param instanceof Array) {
                for (var i = 0; i < param.length; i++) {
                    if (param[i] == val) {
                        return true;
                    }
                }
            } else {
                return param == val;
            }
            return false;
        },
        $.validator.format("所选文件的格式错误！请选择{0}、{1}、{2}、{3}...格式的文件")
    );
    // 校验只能输入下划线、字母或数字，且不能以数字开头
    $.validator.addMethod(
        "check_LetterNum0",
        function(value, element, param){
            if (this.optional(element)) {
                return false;
            }
            if (/^\w+$/.test(value)) { // 判断是否为下划线、字母及数字
                if (/^\d+.*$/.test(value)) { // 判断是否为数字开头
                    return false;
                }
                return true;
            }
            return false;
        },
        $.validator.format("请输入下划线、字母或数字，且不能以数字开头")
    );
})