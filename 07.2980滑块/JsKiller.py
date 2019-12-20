import execjs
import requests
import time



print(time.time())

class douyiSlider():

    def __init__(self,appid,token):
        self.appid = appid
        self.token = token
        self.Header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        self.time = None
        self.background = ""
        self.jigsaw = ""
        self.sn = ""
        self.dif = ""
        self.seed = None

    def Slider_register(self):
        url = "https://www.2980.com/v6/proxy/common/slider_register"
        param = {
            'randomData':self.util_timestamp(),
            'params[deviceUid]':'28ee2f9c06e04a4ca7dc25b323f53072'
        }
        obj = requests.get(url,param,headers = self.Header).json()
        self.token = obj['message']['token']
        self.appid =  obj['message']['appid']
        print('----------------------\n'
              'token - {} \n'
              'appid - {}\n'
              '----------------------'.format(self.token,self.appid))

        if self.token is not None and self.appid is not None:
            return True
        else:
            return False



    def getCaptcha(self):
        url = "https://captcha.duoyi.com/captcha"
        self.time = self.util_timestamp()
        value = "2d0e78f77dea5446be611661d2195041,8451e8c48d9011dd04c77b3e61c5a7bf",
        key = "490ede637f484fd" + str(self.time)
        key = key[8:24]
        param = {
            'token':self.token,
            'appid':self.appid,
            'type':1,
            't':self.time,
            'k':self.AES_Enctypt(value,key)
        }
        obj = requests.get(url,param,headers = self.Header).json()
        self.background = obj['message']['background']
        self.jigsaw = obj['message']['jigsaw']
        self.sn = obj['message']['sn']
        self.dif = obj['message']['dif']
        if self.dif == "0":
            self.seed = "10"
        if self.dif == "1":
            self.seed = self.GetSeed()
        print('Seed - ' + str(self.seed))
        print('----------------------\n'
              'background - {} \n'
              'jigsaw - {}\n'
              'sn  - {}\n'
              'dif - {}\n'
              '----------------------'.format(self.background, self.jigsaw,self.sn,self.dif))

    def Check(self):
        slider = input("slider:")
        portion = input("portion:")
        portion_ = (int(portion) -7)/320
        self.time =self.util_timestamp()
        _0x51e0f8 = "{}:{}:{}".format(portion_,self.time,self.token)
        _0x51e0f8 = self.MD5_Enctypt(_0x51e0f8)
        time = self.util_timestamp10()
        cn = self.MD5_Enctypt(time)
        sign = "{}:{}:{}:{}:{}:{}".format(_0x51e0f8,self.sn,1,cn,"auth","5b350044ac092f7bf3c2bc791638ca2f")
        print('Sign - ' + sign )
        sign = self.MD5_Enctypt(sign)
        print('Sign - ' + sign)
        url = "https://captcha.duoyi.com/check"
        param = {
            "token":self.token,
            "appid":self.appid,
            "portion":portion_,
            "cn":cn,
            "timestamp":self.time,
            "signature":sign,
            "sn":self.sn,
            "seed":self.seed
        }
        key = "490ede637f484fd" +self.time
        key = key[8:24]

        data= '{"browserMsg":{"platform":"Win32","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36","cookieEnabled":1,"hardwareConcurrency":20,"language":"zh-CN","deviceMemory":8,"plugins":[{"description":"Portable Document Format","filename":"internal-pdf-viewer","name":"Chrome PDF Plugin"},{"description":"","filename":"mhjfbmdgcfjbbpaeojofohoefgiehjai","name":"Chrome PDF Viewer"},{"description":"","filename":"internal-nacl-plugin","name":"Native Client"}],"screen":{"availWidth":1920,"availHeight":1040,"width":1920,"height":1080,"colorDepth":24,"pixelDepth":24,"availLeft":0,"availTop":0,"orientation":{}},"webdriver":0,"selenium_$cdc":0,"webglRender":"ANGLE (NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0)","webglVendor":"Google Inc.","canvasMsg":"56ca316b10f509aeb18811d22931dd29","isSWbrowser":0},"localIP":"10.12.161.16","browserUUID":"1c8cc4b0c0aff187bd28ccac5ad5febd",' \
              '"slide":slider,"click_behavior":[],"click_cancel_behavior":[],' \
              '"portion":portion___,"cost_time":"0.5","fingerPrinterList":[25165824,1,"2d0e78f77dea5446be611661d2195041"],"fingerPrinterSon":"8451e8c48d9011dd04c77b3e61c5a7bf","netDuration":5580,"locationHref":"https://www.2980.com/login?callback=/"}'

        data = data.replace("slider",slider).replace("portion___",portion)


        str = requests.post(url,params = param,data=self.AES_Enctypt(data,key)).text
        print(str)
    def GetSeed(self):
        with open('seed.js', 'r') as f:
            JsCode = f.read()

        ctx = execjs.compile(JsCode)
        result = ctx.call('_0x3e9ef9', self.sn,1)
        print(result)
        return result
    def MD5_Enctypt(self,value):
        with open('md5.js', 'r') as f:
            JsCode = f.read()

        ctx = execjs.compile(JsCode)
        result = ctx.call('MD5_Encrypt', value)
        print(result)
        return result
    def AES_Enctypt(self,value,key):
        print('----------------')
        print('AES - Value:' + str(value))
        with open('AES_Enctypt.js', 'r') as f:
            JsCode = f.read()

            JsCode = JsCode.replace("7f484fd157682808",key)

        ctx = execjs.compile(JsCode)
        result = ctx.call('AES_Encrypt', value)
        print(result)
        return result
    def util_timestamp(self):
        return str(int(round(time.time() * 1000)))
    def util_timestamp10(self):
        return str(int(time.time()))


douyi = douyiSlider("","")
douyi.Slider_register()
douyi.getCaptcha()

douyi.Check()