# JsKiller - 07.高级 - 2980滑块验证码破解【未完结】

> 实验地址: https://www.2980.com/login?callback=/

## 1.抓包分析

首先我们先激活滑块,我们先手动验证一次(不必正确,我们只是看看有什么参数进行了加密.)

然而发现网页有反调试.我这里的解决方案是打开抓包工具,在Console中输入以下代码且执行. 就可以过掉这个反调试.

	var _constructor = constructor;
	Function.prototype.constructor = function(s) {
	                if (s == "debugger"){
	                        console.log(s);
	                        return null;
	                }
	       return _constructor(s);
	}



#### 1. 获取验证码图片

	https://captcha.duoyi.com/captcha?token=e07fd64d0331b450d04af368d88a1d7b&appid=227f56ca8543b6826616eea7d6b19f71&type=1&t=1576773601871&k=sJlzCUttW1ANwWdpqbHxSD%2B6QtLcCrQnGHRHs2GotEGHl1ODrVAOCre2bw2b52ibvS4L58bXcQOzRjFQNeFT6EYu7oqpFAgXVvU9MXxlpBM%3D

其中它需要提交的参数信息:

	token: e07fd64d0331b450d04af368d88a1d7b
	appid: 227f56ca8543b6826616eea7d6b19f71
	type: 1
	t: 1576773601871
	k: sJlzCUttW1ANwWdpqbHxSD+6QtLcCrQnGHRHs2GotEGHl1ODrVAOCre2bw2b52ibvS4L58bXcQOzRjFQNeFT6EYu7oqpFAgXVvU9MXxlpBM=
		
token,appid都是固定的.t是timestamp, 剩下一个k值是我们未知的.干他.定位代码

	}, 0x12c);
	var _0x2c286f = new Date()[_0x2181('0xab8')]()
	  , _0x21c983 = _0x381b76[_0x2181('0xc02')](_0x2b2b4b, _0x3c0afb, _0x381b76[_0x2181('0xbaa')](_0x381b76[_0x2181('0xbaa')](fingerPrinterList[0x2], '\x2c'), fingerPrinterSon), _0x381b76[_0x2181('0xbaa')](_0x4c0f02, _0x2c286f)[_0x2181('0xb7d')](0x8, 0x18));
	$[_0x2181('0x2b')]({
	    '\x75\x72\x6c': _0x381b76[_0x2181('0xbaa')](_0x196116[_0x2181('0xe41')], _0x381b76[_0x2181('0xc03')]),
	    '\x64\x61\x74\x61': {
	        '\x74\x6f\x6b\x65\x6e': _0x196116[_0x2181('0x96')],
	        '\x61\x70\x70\x69\x64': _0x196116[_0x2181('0x3d1')],
	        '\x74\x79\x70\x65': _0x196116[_0x2181('0xe48')],
	        '\x74': _0x2c286f,
	        '\x6b': _0x21c983 // '\x6b'就是k
	    },

阅读上面代码,_0x21c983就是K值,那么我们其实要分析下面代码的数据.我们下断点.看看是啥信息.这边建议的操作方式是下断点.一点一点看.

	_0x21c983 = _0x381b76[_0x2181('0xc02')](_0x2b2b4b, _0x3c0afb, _0x381b76[_0x2181('0xbaa')](_0x381b76[_0x2181('0xbaa')](fingerPrinterList[0x2], '\x2c'), fingerPrinterSon), _0x381b76[_0x2181('0xbaa')](_0x4c0f02, _0x2c286f)[_0x2181('0xb7d')](0x8, 0x18));

这边我格式化了一下,让他可视化一点

	_0x381b76[_0x2181('0xc02')](
		_0x2b2b4b,
		 _0x3c0afb, 
		_0x381b76[_0x2181('0xbaa')](_0x381b76[_0x2181('0xbaa')](fingerPrinterList[0x2], '\x2c'), fingerPrinterSon), 
		_0x381b76[_0x2181('0xbaa')](_0x4c0f02, _0x2c286f)[_0x2181('0xb7d')](0x8, 0x18)
	);
		
分析结果:

	_0x2b2b4b:一个函数
	_0x3c0afb:一个函数
	参数3:2d0e78f77dea5446be611661d2195041,8451e8c48d9011dd04c77b3e61c5a7bf
	参数4:ebf54de157677378

咱先分析参数3和参数4

参数3:

	_0x381b76[_0x2181('0xbaa')](_0x381b76[_0x2181('0xbaa')](fingerPrinterList[0x2], '\x2c'), fingerPrinterSon)

	参数1 _0x381b76[_0x2181('0xbaa')](fingerPrinterList[0x2], '\x2c'):2d0e78f77dea5446be611661d2195041
		其中fingerPrinterList[0x2]的值:2d0e78f77dea5446be611661d2195041
	参数2 fingerPrinterSon:8451e8c48d9011dd04c77b3e61c5a7bf

所以这边的小参数1我们其实是要fingerPrinterList[0x2]
通过搜索fingerPrinterList,可以找到

	fingerPrinterList = [browserVersionBinaryNum, browserType, webglAndFontList];

webglAndFontList = 2d0e78f77dea5446be611661d2195041

经过反复的测试，2d0e78f77dea5446be611661d2195041和8451e8c48d9011dd04c77b3e61c5a7bf是固定的。

`_0x381b76[_0x2181('0xbaa')](_0x381b76[_0x2181('0xbaa')](fingerPrinterList[0x2], '\x2c'), fingerPrinterSon)`其实是个是个加法。
拼凑成：`2d0e78f77dea5446be611661d2195041,8451e8c48d9011dd04c77b3e61c5a7bf`

参数4：也是固定的  ebf54de157677378

	_0x105dd2 = _0x47e17f[_0x1e53('0xbb9')](md5, _0x47e17f[_0x1e53('0xbba')](_0x47e17f[_0x1e53('0xbbb')](_0x47e17f[_0x1e53('0xbbb')](_0x47e17f[_0x1e53('0xbbc')], _0x47e17f[_0x1e53('0xbb9')](parseInt, _0x47e17f[_0x1e53('0xbbd')](0x989680, _0x47e17f[_0x1e53('0xbbe')](0xf4240, Math[_0x1e53('0xaa1')]())))), _0x47e17f[_0x1e53('0xbbf')]), new Date()[_0x1e53('0xa2e')]()))


## 未完结，验证暂时未通过。可能有的细节没处理完。 明日面试后继续看！
## 面试加油哇

	