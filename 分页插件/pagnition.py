class PageInfo(object):
    def __init__(self, current_page, all_count, base_url, page_param_dict, per_page=10, show_page=11):
        """

        :param current_page: 当前页
        :param all_count: 总页数
        :param base_url: 模板
        :param page_param_dict: QueryDict对象，封装了当前url的get参数，确保在生成分页url时保留get参数
        :param per_page: 每页显示数据条数
        :param show_page: 显示链接页个数
        """
        # 若url错误，默认显示第一页（错误类型可能为：空页面编号，非整数型页面编号）
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1

        # 根据数据库信息条数得出总页数
        a, b = divmod(all_count, per_page)
        if b:
            a += 1
        self.all_page = a

        self.base_url = base_url
        self.per_page = per_page
        self.show_page = show_page
        self.page_param_dict = page_param_dict

    # 当前页起始数据id
    @property
    def start_data(self):
        return (self.current_page - 1) * self.per_page

    # 当前页结束数据id
    @property
    def end_data(self):
        return self.current_page * self.per_page

    # 动态生成前端html
    def pager(self):
        page_list = []
        half = int((self.show_page - 1) / 2)
        # 如果：总页数 < show_page，默认显示页数范围为： 1~总页数
        if self.all_page < self.show_page:
            start_page = 1
            end_page = self.all_page + 1
        # 如果：总页数 > show_page
        else:
            # 如果：current_page - half <= 0，默认显示页数范围为：1~show_page
            if self.current_page <= half:
                start_page = 1
                end_page = self.show_page + 1
            else:
                # 如果：current_page + half >总页数，默认显示页数范围为：总页数 - show_page ~ 总页数
                if self.current_page + half > self.all_page:
                    end_page = self.all_page + 1
                    start_page = end_page - self.show_page
                else:
                    start_page = self.current_page - half
                    end_page = self.current_page + half + 1

        # 首页
        self.page_param_dict['page'] = 1
        first_page = "<li><a href='%s?%s'>首页</a></li>" % (self.base_url, self.page_param_dict.urlencode())
        page_list.append(first_page)

        # 上一页
        if self.current_page <= 1:
            prev_page = "<li><a href='#'>上一页</a></li>"
        else:
            self.page_param_dict['page'] = self.current_page - 1
            prev_page = "<li><a href='%s?%s'>上一页</a></li>" % (self.base_url, self.page_param_dict.urlencode())
        page_list.append(prev_page)

        # 动态生成中间页数链接
        for i in range(start_page, end_page):
            self.page_param_dict['page'] = i
            if i == self.current_page:
                temp = "<li class='active'><a href='%s?%s'>%s</a></li>" % (
                    self.base_url, self.page_param_dict.urlencode(), i)
            else:
                temp = "<li><a href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(), i)
            page_list.append(temp)

        # 下一页
        if self.current_page >= self.all_page:
            next_page = "<li><a href='#'>下一页</a></li>"
        else:
            self.page_param_dict['page'] = self.current_page + 1
            next_page = "<li><a href='%s?%s'>下一页</a></li>" % (self.base_url, self.page_param_dict.urlencode())
        page_list.append(next_page)

        # 末页
        self.page_param_dict['page'] = self.all_page
        if self.all_page > 1:
            last_page = "<li><a href='%s?%s'>末页</a></li>" % (self.base_url, self.page_param_dict.urlencode())
            page_list.append(last_page)

        return ''.join(page_list)
