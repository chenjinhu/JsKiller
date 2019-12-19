# JsKiller - 04.飞卢网

>操作地址: https://u.faloo.com/Regist/Login.aspx?txtUserID=1354477&txtPwd=a38579d27a7860c2aea5aab5bf9af073&txtPwd4temp=&verifyCode=j4bb&ts=1576728695&t=2&backurl=http%3A%2F%2Fwww.faloo.com%2F
>卑微弟弟在线求Star

## 01.抓包分析
打开抓包工具抓包分析.可以找到**Login.aspx**包,其中提交的数据`txtPwd`进行了加密.我们今天的目标就是这个参数

## 02.破解
看着形状,形似md5,去搜索看看>
在Search窗口搜索`txtPwd`. login.asp文件中找到以下代码

    document.faloo_login.backurl.value = backurl;
    var time_stamp =1576728829;//  get_timestamp();
    document.faloo_login.ts.value = time_stamp;
    pwd = login_md5(pwd, time_stamp);
    document.faloo_login.txtPwd.value = pwd;
    document.faloo_login.txtPwd4temp.value = "";
    document.faloo_login.action = "Login.aspx?t=2&BackUrl=" + backurl + "&ran=" + Math.random();
    document.faloo_login.method = "get";
    document.faloo_login.submit();
    document.faloo_login.txtPwd4temp.value = pwd4temp;

通过阅读代码.我们可以知道`txtPwd -> pwd -> login_md5`
所以,我们找login_md5函数.下断激活.

	var hexcase = 0;
	var b64pad = "";
	var chrsz = 8;
	function hex_md5(s) { return binl2hex(core_md5(str2binl(s), s.length * chrsz)); }
	function b64_md5(s) { return binl2b64(core_md5(str2binl(s), s.length * chrsz)); }
	function hex_hmac_md5(key, data) { return binl2hex(core_hmac_md5(key, data)); }
	function b64_hmac_md5(key, data) { return binl2b64(core_hmac_md5(key, data)); }
	function calcMD5(s) { return binl2hex(core_md5(str2binl(s), s.length * chrsz)); }
	function login_md5(pwd, datetime_num) { return hex_md5("@345Kie(873_dfbKe>d3<.d23432="+hex_md5("EW234@![#$&]*{,OP}Kd^w349Op+-32_" + pwd + datetime_num)); }
	function get_timestamp() { return (new Date()).valueOf();}//时间戮
	function core_md5(x, len) {


上面这个代码非常好,完全不用改写哦.这就是一个完整的md5包.咱可以直接调用.


## 03.调用

代码可以已上传至github.
	
	import execjs
	
	with open('feilu.js','r') as f:
	    JsCode = f.read()
	print(JsCode)
	
	ctx = execjs.compile(JsCode)
	result = ctx.call('login_md5',"github",'1576728829')
	print(result)
	

