# 使用方法：
## Django
1. 视图函数中导入分页插件
`from your_plugins_path.pagnition import PageInfo`
2. 实例化PageInfo
`page_obj = PageInfo(current_page=request.GET.get('page'), all_count=all_count, base_url=base_page_url, page_param_dict=page_param_dict)`
3. 获取当前页展示信息
`current_page = self.model_class.objects.filter(**conditions)[page_obj.start_data:page_obj.end_data]`
4. 返回结果给模板
`return render(request, 'dap/change_list.html', {'current_page': current_page, 'page_str': page_obj.pager()})`
5. HTML中使用（结合Bootstrap修饰）
```<ul class="pagination">
	{{ page_str|safe }}
</ul>```
