# v2exDaily
a daily program for v2ex.com

使用requests模拟v2ex网站的登陆及签到功能，将对应源文件v2exDaily.py存放到本地直接python运行即可


---

依赖库:
- requests
- bs4
- pytesseract

---
更新日志：
> 11/11 新增对于验证码的识别，获取到的验证码会保存在脚本运行同级目录下（./captcha.jpg）

> 11/15 鉴于pytesseract识别验证码并未百分百正确，新增手工填写验证码的步骤，若想依然使用自动识别得结果，直接回车即可
