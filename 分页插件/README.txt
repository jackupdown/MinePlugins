使用方法：
	一、Django
		1. 视图函数中导入分页插件
			例如：from your_plugins_path.pagnition import PageInfo
		2. 实例化PageInfo
			例如：page_obj = PageInfo(current_page=request.GET.get('page'), all_count=all_count, base_url=base_page_url, page_param_dict=page_param_dict)
		3. 获取当前页展示信息
			例如：current_page = self.model_class.objects.filter(**conditions)[page_obj.start_data:page_obj.end_data]
		4. 返回结果给模板
			例如：return render(request, 'dap/change_list.html', {'current_page': current_page, 'page_str': page_obj.pager()})
		5. HTML中使用（结合Bootstrap修饰）
			例如：
				<ul class="pagination">
					{{ page_str|safe }}
				</ul>