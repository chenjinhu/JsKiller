import execjs

with open('wx.js','r') as f:
    JsCode = f.read()
print(JsCode)

ctx = execjs.compile(JsCode)
result = ctx.call('JsKiller','github')
print(result)
