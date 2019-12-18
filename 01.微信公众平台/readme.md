# JsKiller - 01.微信公众平台

> github地址：https://github.com/chenjinhu/JsKiller 求Star
> 破解参数：pwd（登录步骤）
> 环境：Windows10/Google Chrome


## 1. 抓包分析

F12打开 开发者工具, 刷新页面,执行登录操作.

很容易发现在**bizlogin?action=startlogin** 可以找到pwd参数.这就是我们今天的目标.

## 2. 破解

在Search功能栏下搜索**pwd**
很快可以定位到以下代码

    _loginPost: function(e, i) {
        n.post({
            url: i.url,
            data: {
                username: i.account,
                pwd: o(i.pwd.substr(0, 16)), // 关键代码
                imgcode: i.verify,
                f: "json",
                userlang: i.currentLang,
                redire

我们在`pwd: o(i.pwd.substr(0, 16))`行处下断点。然后步入进去.

    t.exports = function(n, r, t) {
        return r ? t ? c(r, n) : function(n, r) {
            return e(c(n, r))
        }(r, n) : t ? o(n) : function(n) {
            return e(o(n)) // *****
        }(n)
    }

继续步入一次，代码最后会走到我标*的地方。这就是我们需要的关键函数,扣代码吧。

扣下代码。然后自己编写一个Js function

	function JsKiller(pwd){
		return e(o(pwd));
	}

## 3.调用
wx.js文件自行下载参考即可。

	import execjs
	
	with open('wx.js','r') as f:
	    JsCode = f.read()
	print(JsCode)
	
	ctx = execjs.compile(JsCode)
	result = ctx.call('JsKiller','github')
	print(result)
	

