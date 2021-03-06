# RBAC-基于角色的权限管理
是一个基于Django开发的app，用于解决通用权限管理。
## 使用方法：
1. 在settings配置文件中注册App，即：rbac
    ```
	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    ...
	    'rbac',
	]
    ```

2. 在settings配置文件中引入rbac用于权限控制中间件
    ```
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'rbac.middleware.rbac.RbacMiddleware',
    ]
    ```
3. 在settings配置文件中设置rbac需要的配置

* 3.1. 无需权限控制的URL
	```
	RBAC_NO_AUTH_URL = [
		'/index.html',
		'/login.html',
		'/register.html',
		'/admin.*',
		...
	]
	```

* 3.2. Session中保存权限信息的Key

	`RBAC_PERMISSION_SESSION_KEY = "rbac_permission_session_key"`

	`注意：登录时，获取当前用户权限信息并保存在该Session中，以后每次访问时，都会在中间件中根据此Key去Session获取权限信息并判断`
    
* 3.3. Session中保存菜单和权限信息的Key
	```
	RBAC_MENU_PERMISSION_SESSION_KEY = "rbac_menu_permission_session_key"
	RBAC_MENU_KEY = "rbac_menu_key"
	RBAC_MENU_PERMISSION_KEY = "rbac_menu_permission_key"

	注意：登录时，获取当前用户菜单以及权限并保存在Session中，用于自动创建当前用户菜单
	```

* 3.4. 菜单主题

	`RBAC_THEME = "default"`
	
	`注意：自动创建当前用户菜单时指定的主题`

* 3.5. Http请求中传入的参数，根据其获取GET、POST、EDIT等检测用户是否具有相应权限，例如：
	```
	http://www.example.com?md=get   表示获取
	http://www.example.com?md=post  表示添加
	http://www.example.com?md=delete   表示删除

	RBAC_QUERY_KEY = "md"
	```

* 3.6. 无权访问时，页面提示信息

	`RBAC_PERMISSION_MSG = "无权限访问"`

4. 在数据库中创建用户、角色、权限、菜单以及分配相应权限

5. 用户登录

	用户登录成功，需要初始化权限以及菜单信息，如：
	```
    from rbac.service import initial_permission
    initial_permission(request, user_id)
    * request指当前请求对象
    * user_id指rbac表中的user_id
	```
    示例：
	```
	def login(request):
	    if request.method == "GET":
		return render(request, 'login.html')
	    else:
		user = request.POST.get('username')
		pwd = request.POST.get('password')
		print(user, pwd)
		obj = models.UserInfo.objects.filter(user__username=user, user__password=pwd).first()
		print(obj)
		if obj:
		    initial_permission(request, obj.user.id)
		    return redirect('/index.html')
		else:
	    return render(request, 'login.html', {'msg': '用户名或密码错误'})
	```

    `注意：默认rbac的用户表只有username、password、email字段，如果想要扩展更多，可以通过OneToOneField进行关联`
    
	```
	class UserInfo(models.Model):
	    nickname = models.CharField(max_length=32)
		user = models.OneToOneField(RbacModels.User)
	```

6. 开发业务功能，如：
* 6.1 FBV：
	```
	def xxoo(request):
		if request.permission_code == "GET":
			# 查看权限
			pass
		elif request.permission_code == "POST":
			# 添加权限
			pass
		elif request.permission_code == "PUT":
			# 修改权限
			pass
		elif request.permission_code == "DELETE":
			# 删除权限
			pass

		print(request.permission_code)
		print(request.permission_code_list)

		return HttpResponse('订单')
	```
	```
	PS： 在需要权限才能访问的视图中，通过request.permission_code获取当前用户对此URL的权限
		 权限对应的值由数据库的action中的code字段指定；通过request.permission_code_list获取当前用户拥有的所有权限
	```

* 6.2 CBV：
	```
	from django.views import View
	from rbac.cbv.views import RbacView

	class OrderView(RbacView, View):
		def get(self, request, *args, **kwargs):
			# 查看权限
			pass

		def delete(self, request, *args, **kwargs):
			# 添加权限
			pass

		def put(self, request, *args, **kwargs):
			# 修改权限
			pass

		def delete(self, request, *args, **kwargs):
			# 删除权限
			pass
	```

7. 展示当前用户所有菜单
```
    {% load rbac %}                     <!-- 导入rbac中提供的模板方法 -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <style>
            {% rbac_css %}              <!-- 导入rbac中为菜单提供的样式 -->
        </style>
    </head>
        <body>
            <div style="width: 200px;float: left">
                {% rbac_menu request %} <!-- 导入rbac中创建的当前用户菜单 -->
            </div>

            <div style="float: left">
                欢迎登录
            </div>

            <script src="/static/jquery-1.8.2.min.js"></script>
            <script>
                $(function () {
                    {% rbac_js %}       <!-- 导入rbac中为菜单提供的js -->
                });
            </script>
        </body>
    </html>
```

