# JsKiller - 02.拍拍贷

>操作地址: http://www.aipai.com/
>卑微弟弟在线求Star

## 01.抓包分析
打开抓包工具抓包分析.可以找到**login.php**包,其中提交的数据`password`进行了加密.我们今天的目标就是这个参数

## 02.破解
在Search窗口搜索`password`.我们可以在header.js文件中找到2处调用了` _ts.md5`方法的地方.大家可以把这些位置都下断点.

	 action = action || 'loginNew';
	        metadata = 'action=' + action + '&account=' + user + '&password=' + _ts.md5(pass) + '&keeplogin=' + keep + '&comouterTime=' + keep + '&userNowTime=' + userNowTime;
	        var _host = location.host;
	        if (_host == "www.aipai.com") {
	            loginUrl = "/login.php";
	            metadata = 'action=' + action + '&user=' + user + '&password=' + _ts.md5(pass) + '&keeplogin=' + keep + '&comouterTime=' + keep + '&userNowTime=' + userNowTime;
	        }

阅读上面的代码. 我们可以很轻松的知道了加密位置, 那么我们下断点进去,然后激活断点(登录一下).
我们进入_ts.md5,把md5函数拿下来

	 md5: function(value) {
	        var hex_chr = "0123456789abcdef"
	          , rhex = function(num) {
	            var str = "";
	            for (j = 0; j <= 3; j++)
	                str += hex_chr.charAt((num >> (j * 8 + 4)) & 0x0F) + hex_chr.charAt((num >> (j * 8)) & 0x0F);
	            return str;

然后改写一下.

	function md5(value)


## 03.调用

代码可以已上传至github.

	import execjs
	
	with open('aipai.js','r') as f:
	    JsCode = f.read()
	print(JsCode)
	
	ctx = execjs.compile(JsCode)
	result = ctx.call('md5',"github")
	print(result)
	

