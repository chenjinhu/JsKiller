# JsKiller - 02.拍拍贷

>操作地址: http://suo.im/6bpNpv
>卑微弟弟在线求Star

## 01.抓包分析
打开抓包工具抓包分析.可以找到**securityWeb?appid=1000002180**包,其中提交的数据`password`和`phone`都是进行了加密.我们今天的目标就是这2个参数

## 02.破解
在Search窗口搜索`password`.我们可以在newsdk....js文件中找到多处调用了`e.$encrypt.encrypt()`方法的地方.大家可以把这些位置都下断点.

    if (!e.reg_iAgree)
        return void (e.reg_errormsg = "请阅读并同意相关服务协议");
    var r = {
        authCode: e.reg_phonecode,
        extraInfo: e.$parent.getExtraInfo(),
        password: e.$encrypt.encrypt(e.md5(e.reg_password)),
        phone: e.$encrypt.encrypt(e.reg_mobile),
        sourceId: e.sourceId,
        userRole: e.userRole
    };
    if (0 == e.userRole)
        return void (e.showSdkDialog = !0);
    e.reg_submit = "正在提交中...",

阅读上面的代码. 我们可以很轻松的知道了加密位置, 那么我们下断点进去,然后激活断点(登录一下).
我们先进入e.md5,把md5函数拿下来

    function r(e) {
        return o(i(a(e)))
    }

然后我们再来把`e.$encrypt.encrypt`函数拿下来

    e.prototype.encrypt = function(e) {
        try {
            return l(this.getKey().encrypt(e))
        } catch (e) {
            return !1
        }
    }



## 03.调用
