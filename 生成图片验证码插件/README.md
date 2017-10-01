# Django用法
## views.py
```
def check_code(request):
    """
    生成图片验证码
    :param request:
    :return:
    """
    img, code = rd_check_code()
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())
```	
## urls.py
`url(r'^check-code/', homeViews.check_code),      # 获取验证码`
## test.html
```
<img onclick="changImg(this);" src="/check-code/" title="点击更换" style="width: 150px; height: 30px">

function changImg(self) {
  self.src=self.src+"?";
}
```
ps. 字体文件kumo.ttf请先放于项目的根目录下，否则插件会找不到字体文件而出错