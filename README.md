# SITBishe2020

![2](https://user-images.githubusercontent.com/18359157/122680684-01c04c00-d223-11eb-80ad-9bcac35b07b4.png)

## What's this

这个是我2020年水的毕业设计...

当时抽到了个“信息系统”的题目，为了搞起来不这么无聊，顺便想试试用[SQLike](https://github.com/liyafe1997/SQLike) & Python的http.server能不能搞出个看起来有模有样的东西

前端用的Vue.js，UI用的一个叫Vue Material Dashboard的模板。FrontEnd/bms_webpage是一个webpack项目，你可以npm update/npm run build生成dist。

另，如果你想方便debug，可以在Webserver下把WEBCONTENT目录symbol link到 ../FrontEnd/bms_webpage/dist

答案是看起来似乎是可以的...各位也别笑话

总之，水的一个东西，一是为了毕业设计，二是Just for fun.

# 食用方法

1. 先把SQLike数据库跑起来，注意要开server模式
```
cd SQLike
python3 SQLike.py server 127.0.0.1 1234
```

2. 把Webserver跑起来

（注：你可能要先安装PyJWT: pip3 install PyJWT），注意是PyJWT而不是jwt！

```
cd Webserver
python3 webserver.py
```

3. 浏览器访问127.0.0.1:8081应该就出来了

用户名admin密码admin应该就能进去了

![1](https://user-images.githubusercontent.com/18359157/122680617-ae4dfe00-d222-11eb-9a6a-5fedf81bcd43.png)
