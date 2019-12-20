# JsKiller - 06.毛毛租【未完结】

> 网址 : https://www.maomaozu.com/#/build


## 1.抓包分析
打开抓包工具.抓取bulid.json包.发现都是一堆乱七八糟的内容.

	LqokFArgAdpTEyDbREHFofZLZkhPofBKGuoTJbTN+xZw6ntNVMhd5OaWrCECvIbAmHeP+jIC1ZrjOY7QaxyWSIXitOcJlZ90drOZVrPOm66RHtLUi2G7yysTqQD/Ys1iqiF3CpNfVpHv7njPvMGNSWj/uR7RKrcrHqUN6+nwSgOpCMcYS5KAOEfRpYDnUP3fyo9LEXwuvbj4omkoOFhmPnz4Eux
上面数据不止这么一点长度.这乍一看,無法下手呀~

## 2.破解
根据经验,我们可以判断,该网站肯定是有**decrypt**的地方.同时可以猜测它可能是 `AES,DES,3DES,RSA`等算法.因为真的神似.所以搜索下关键词`decrypt`

	aes_decrypt: function(e) {
		var l = this.k(0).split("").reverse().join("");
		return this.d(l, e)
	},
结果非常容易定位到上面的内容.下断点.调试

	var l = this.k(0).split("").reverse().join("");



继续向下走,可以走到

    d: function(e, l) {
        e = n.default.enc.Utf8.parse(e);
        var a = n.default.AES.decrypt(l, e, {
            mode: n.default.mode.CBC,
            padding: n.default.pad.Pkcs7,
            iv: e
        });
        return n.default.enc.Utf8.stringify(a).toString()
    }

l变量就是我们的秘钥. 加密方式是AES/PKCS7/CBC (CBC模式只需要Key,不需要iv)
目前可知:
l - 秘钥
e - 密文



