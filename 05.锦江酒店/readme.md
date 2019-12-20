# JsKiller - 05.锦江酒店

- 难度等级:★★
- 网址：https://hotel.bestwehotel.com/NewLogin/?go=https%3A%2F%2Fhotel.bestwehotel.com
- 目标：password/black_box
- 建议完成时间：15分钟


## 1.抓包分析

打开抓包工具，登录。`login`包

## 2.破解1 - password
首先搜索password。经过简单的分析。可以跟到

    encryptAES: function(e) {
        return l(e)
    }
下断，进入l函数

    function l(e) {
        var n = CryptoJS.enc.Latin1.parse("h5LoginKey123456")
          , a = CryptoJS.enc.Latin1.parse("h5LoginIv1234567")
          , t = e
          , o = CryptoJS.AES.encrypt(t, n, {
            iv: a,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.ZeroPadding
        });
        return o.toString()
    }
然后就是扣代码，这代码非常好扣。复制粘贴的事情，这里就不多讲。具体JS代码参考  `password.js`文件

## 3.破解2：black_box

首先我们看下其数据的形状

	eyJ2IjoianJFK1d4Y3N4RVhBb0h1RU16R1Fkd2FmZ2pYTDVCWU14WTBlSndvTUZCZFFSQTZFL29oUGhOLzVTOEY1OFgvOSIsIm9zIjoid2ViIiwiaXQiOjEyNDQyNTQsInQiOiJtbElCTElERGd2UHlyU010YjBQK2xoZUZEb3ZpWHlBcWtQVndIU25Qb3FUTS96cjQ3b2paL1VsdlpkZzZtVkIxYUs3QVpjRkd5SEliTEtzcUFmYUM0bjdqS1FBMkQ1UlAzdjVROEtnckRvbz0ifQ==
这样子的东西，ey开头的一般都是BASE64编码过后的。所以我们BASE64解码。就可以看到下面的数据

	{"v":"jrE+WxcsxEXAoHuEMzGQdwafgjXL5BYMxY0eJwoMFBdQRA6E/ohPhN/5S8F58X/9","os":"web","it":1244254,"t":"mlIBLIDDgvPyrSMtb0P+lheFDoviXyAqkPVwHSnPoqTM/zr47ojZ/UlvZdg6mVB1aK7AZcFGyHIbLKsqAfaC4n7jKQA2D5RP3v5Q8KgrDoo="}

很容易可以定位到下面代码处

	login: function(n) {
	    var a = _fmOpt.getinfo();
	    a && (n.black_box = a);
	    var t = this.getApiPath() + "/login";
	    return e.post(t, n)
	}
然后关键地方是_fmOpt.getinfo();函数生成的内容就是我们要的东西。进去看看，结果发现了下面的混淆。并且还是在VM里面的代码。这时候下断点是没用的。所以我们在`var a = _fmOpt.getinfo()`下断点。然后走进来再下断点。

    oo0oQO: function oo0oQO() {
        o00QQQ[QoQO0o][OOoOQo("x", 0)] = ooQ0Oo[QoOOoQ];
        o00QQQ[QoQO0o][OOQoOo] = OOO0Qo;
        o00QQQ[QoQO0o][O00OOQ] = (new Date)[O0O0oQ]() - OOOQ00;
        if (o00QQQ[o0QooQ] % 255) {
            o00QQQ[QoQO0o][OOoOQo("%", 15)] = o00QQQ[o0QooQ];
            if (!Q0oOQO[oo00OO]()) {
                Ooo0Q0()
            }
            o00QQQ[QoQO0o][OOoOQo("e", 94)] = JSON[QQQoQO](o00QQQ[OoOOoQ])
        } else {
            if (o00QQQ[QoQOOQ]) {
                o00QQQ[QoQO0o][OOoOQo("X", 65)] = o00QQQ[QoQOOQ];
                if (o00QQQ[QoQooO] && o00QQQ[QoQooO] !== "1") {
                    o00QQQ[QoQO0o][OOoOQo("N", 72)] = o00QQQ[QoQooO]
                }
            } else {
                o00QQQ[QoQO0o][OOoOQo(",", 36)] = oOQo0O
            }
        }
        return QQ00oO[oOOQQQ](JSON[QQQoQO](o00QQQ[QoQO0o]))
    }

我的初步解决方案为：
这些代码全复制进来，然后把

	_fmOpt = {
	    partner: '7daysinn',
	    appName: 'jinjianglx_web',
	    token: '7daysinn' + "-" + new Date().getTime() + "-"+ Math.random().toString(16).substr(2),
	    fmb: true,
	    getinfo: function(){
	        return "e3Y6ICIyLjUuMCIsIG9zOiAid2ViIiwgczogMTk5LCBlOiAianMgbm90IGRvd25sb2FkIn0=";
	    }   
也给整进来。这样在浏览器就可以运行成功了。但是这应该过不了验证。更多的等明天面试完再继续看！ 


#面试加油！