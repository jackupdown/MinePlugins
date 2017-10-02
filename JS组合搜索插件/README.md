# JS组合搜索插件
## Django使用方法：
* 在HTML文件中导入(配合JQ和bootstrap插件)：
```
{% block content %}
{% include 'nb-search.html' %}
{% include 'nb-tpl.html' %}
{% endblock %}

{% block js %}
<script src="/static/js/jquery-3.2.1.js"></script>
<script src="/static/plugins/bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>
<script src="/static/js/nb-list.js"></script>

	<script>
	$.init_asset('/backend/server.html/');
	</script>
{% endblock %}
```
## 图示
![]('https://github.com/jackupdown/MinePlugins/tree/master/')