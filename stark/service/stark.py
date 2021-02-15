import functools
from types import FunctionType
from django.urls import reverse
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.http import QueryDict
from django.shortcuts import HttpResponse, render, redirect

from django.db.models import Q
from django.db.models import ForeignKey, ManyToManyField

from stark.utils.pagination import Pagination
from stark.forms.base import StarkModelForm


def get_choice_text(title, field):
    """
    对于Stark组件中定义列，显示choice的中文信息
    :param title: 表头
    :param field: choice字段名称
    :return: 获取该字段值的方法（get_字段_display）
    """

    def inner(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return title
        method = "get_%s_display" % field
        return getattr(obj, method)()

    return inner


def get_datetime_text(title, field, time_format='%Y-%m-%d'):
    """
    对于Stark组件中定义列时，定制时间格式的数据
    :param title: 表头
    :param field: 字段名称
    :param time_format: 要格式化的时间格式
    :return:
    """

    def inner(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return title
        datetime_value = getattr(obj, field)
        return datetime_value.strftime(time_format)

    return inner


def get_m2m_text(title, field):
    """
    对于Stark组件中定义列时，显示多对多关系的文本信息
    :param title: 表头
    :param field: 字段名称
    :return:
    """

    def inner(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return title
        queryset = getattr(obj, field).all()
        text_list = [str(row) for row in queryset]
        return '、'.join(text_list)

    return inner


class SearchGroupRow(object):
    """
    实例化此类时，根据获取到的组合筛选条件，生成带有html标签的可迭代对象
    """

    def __init__(self, title, queryset_or_tuple, option, query_dict):
        """
        :param title: 组合搜索的列名称
        :param queryset_or_tuple: 组合筛选条件
        :param option: 配置
        :param query_dict: request.GET，包含当前选中的所有option信息
        """
        self.title = title
        self.queryset_or_tuple = queryset_or_tuple
        self.option = option
        self.query_dict = query_dict

    def __iter__(self):
        """
        增加迭代器方法，以在html文件中通过循环渲染标签
        :return:
        """
        yield '<div class="whole">'
        yield self.title
        yield '</div>'

        yield '<div class="others">'
        # 获取所有get请求
        query_dict = self.query_dict.copy()
        query_dict._mutable = True

        # 获取get请求中option对应字段的值，如：depart=1&depart=2时，origin_value_list=[1,2,]
        origin_value_list = self.query_dict.getlist(self.option.field)

        # get请求中没有当前属性的组合筛选，全选按钮活跃
        if not origin_value_list:
            yield "<a class='active' href='?%s'>全部</a>" % query_dict.urlencode()
        # get请求中有当前属性的组合筛选
        else:
            # 点击全选后，只清空当前属性的筛选条件
            query_dict.pop(self.option.field)
            yield "<a href='?%s'>全部</a>" % query_dict.urlencode()

        for item in self.queryset_or_tuple:
            # 显示文本
            text = self.option.get_text(item)
            # id值
            value = str(self.option.get_value(item))
            # 重新获取所有get请求
            query_dict = self.query_dict.copy()
            query_dict._mutable = True

            # 单选
            if not self.option.is_multi:
                # 1
                query_dict[self.option.field] = value
                # 实现toggle选中
                if value in origin_value_list:
                    # 已选中的，点击后取消选中
                    query_dict.pop(self.option.field)
                    yield "<a class='active' href='?%s'>%s</a>" % (query_dict.urlencode(), text)
                else:
                    # 未选中的，点击后选中
                    yield "<a href='?%s'>%s</a>" % (query_dict.urlencode(), text)
            # 支持多选
            else:
                # [1, 2, ]
                multi_value_list = query_dict.getlist(self.option.field)
                # 实现toggle选中
                if value in multi_value_list:
                    # 已选中的，点击后取消选中
                    multi_value_list.remove(value)
                    query_dict.setlist(self.option.field, multi_value_list)
                    yield "<a class='active' href='?%s'>%s</a>" % (query_dict.urlencode(), text)
                else:
                    # 未选中的，点击后选中
                    multi_value_list.append(value)
                    query_dict.setlist(self.option.field, multi_value_list)
                    yield "<a href='?%s'>%s</a>" % (query_dict.urlencode(), text)

        yield '</div>'


class Option(object):
    """
    组合筛选配置类
    """

    def __init__(self, field, is_multi=False, db_condition=None, text_func=None, value_func=None):
        """
        :param field: 组合搜索关联的字段
        :param is_multi: 是否支持多选
        :param db_condition: 控制显示哪些组合筛选的条件
        :param text_func: 显示组合搜索按钮页面文本
        :param value_func: 显示组合搜索按钮值
        """
        self.field = field
        self.is_multi = is_multi
        if not db_condition:
            db_condition = {}
        self.db_condition = db_condition
        self.text_func = text_func
        self.value_func = value_func
        self.is_choice = False

    def get_db_condition(self, request, *args, **kwargs):
        """
        预留钩子：数据库关联查询时的搜索条件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.db_condition

    def get_queryset_or_tuple(self, model_class, request, *args, **kwargs):
        """
        根据字段去获取数据库关联的数据
        :return:
        """
        # 根据字段名找到字段对象
        field_object = model_class._meta.get_field(self.field)
        title = field_object.verbose_name
        # 获取外键或多对多关联数据
        if isinstance(field_object, ForeignKey) or isinstance(field_object, ManyToManyField):
            db_condition = self.get_db_condition(request, *args, **kwargs)
            # 组合筛选条件，QuerySet类型，Django3.0以上版本，外键查询不支持rel，使用remote_field
            queryset_or_tuple = field_object.remote_field.model.objects.filter(**db_condition)
            # 返回带有html标签的可迭代对象
            return SearchGroupRow(title, queryset_or_tuple, self, request.GET)

        # 获取choice中的数据
        else:
            self.is_choice = True
            # 组合筛选条件，如：((1, '男'), (2, '女'))
            queryset_or_tuple = field_object.choices
            # 返回带有html标签的可迭代对象
            return SearchGroupRow(title, queryset_or_tuple, self, request.GET)

    def get_text(self, field_object):
        """
        获取组合筛选的显示文本
        :param field_object: 组合筛选对象或元组
        :return:
        """
        # 预留的钩子方法
        if self.text_func:
            return self.text_func(field_object)

        if self.is_choice:
            # (1, '男') --> '男'
            return field_object[1]

        # 对象的__str__返回值
        return str(field_object)

    def get_value(self, field_object):
        """
        获取组合筛选的对应表的记录id
        :param field_object: 组合筛选对象或元组
        :return:
        """
        # 预留的钩子方法
        if self.value_func:
            return self.value_func(field_object)

        if self.is_choice:
            # (1, '男') --> 1
            return field_object[0]

        # 对象的pk值
        return field_object.pk


class StarkHandler(object):
    """
    stark配置类
    """
    # 预留钩子：html模板
    list_template = None
    add_template = None
    edit_template = None
    del_template = None

    def __init__(self, site, model_class, prev):
        """
        :param site: site对象
        :param model_class: ORM映射
        :param prev: URL前缀
        """
        self.site = site
        self.model_class = model_class
        self.prev = prev
        self.request = None

    # ModelForm配置
    model_form_class = None

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        """
        预留钩子：根据当前访问的页面，初始化对应ModelForm类
            默认展示所有字段，可自定义展示字段
        :param is_add:
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(StarkModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    # 页面上显示的列
    list_display = []

    def get_list_display(self, request, *args, **kwargs):
        """
        获取页面上应该显示的列，预留的自定义扩展，例如：以后根据用户的不同显示不同的列
            默认显示display_edit_del
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_edit_del)
        return value

    def display_checkbox(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义的选择框列
        :param obj: 当前数据对象
        :param is_header: 是否是表头
        :return:
        """
        if is_header:
            return "选择"
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' % obj.pk)

    def display_edit(self, obj=None, is_header=None, *args, **kwargs):
        """
        预留钩子：允许自定义的编辑列
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "选项"
        return mark_safe(
            """
            <div class="pull-right">
                <a class="text-primary" style="margin-right: 10px;" href="%s">
                    编辑
                </a>
            </div>""" % self.reverse_edit_url(pk=obj.pk, *args, **kwargs))

    def display_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        预留钩子：允许自定义的删除列
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "选项"
        return mark_safe(
            """
            <div class="pull-right">
                <a class="text-danger" href="%s">
                    删除
                </a>
            </div>""" % self.reverse_del_url(pk=obj.pk, *args, **kwargs))

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        预留钩子：允许自定义的编辑删除列
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return mark_safe("""
            <div class="pull-right">
                选项
            </div>""")
        tpl = """
            <div class="pull-right">
                <a class="text-primary" style="margin-right: 10px;" href="%s">
                    编辑
                </a>
                <a class="text-danger" href="%s">
                    删除
                </a>
            </div>""" % (
            self.reverse_edit_url(pk=obj.pk, *args, **kwargs), self.reverse_del_url(pk=obj.pk, *args, **kwargs))
        return mark_safe(tpl)

    # 组合搜索范围
    search_group = []

    def get_search_group(self):
        """
        预留钩子：获取组合搜索范围
            默认无组合搜索功能，可自定义添加搜索范围，如：
            search_group = [
                Option('gender', is_multi=True),
                Option('classes'),
                Option('depart', is_multi=True, db_condition={'id__gt': 0}),
            ]
        :return:
        """
        return self.search_group

    def get_search_group_condition(self, request):
        """
        获取组合搜索的条件
        :param request:
        :return: 字典类型的搜索条件
        """
        condition = {}

        for option in self.get_search_group():
            # 支持多选
            if option.is_multi:
                values_list = request.GET.getlist(option.field)  # values_list = [1, 2, ]
                if not values_list:
                    continue
                condition['%s__in' % option.field] = values_list
            # 单选
            else:
                value = request.GET.get(option.field)  # value = 1
                if not value:
                    continue
                condition[option.field] = value

        return condition

    # 关键字搜索范围
    search_list = []

    def get_search_list(self):
        """
        预留钩子：获取关键字搜索范围
            默认无关键字搜索功能，可自定义添加搜索范围，如
            search_list = [
                'name__contains',
                'email__contains',
            ]
        :return:
        """
        return self.search_list

    # 排序方式
    order_list = []

    def get_order_list(self):
        """
        预留钩子：获取排序方式
            默认按id降序排序
        :return:
        """
        return self.order_list or ['-id', ]

    # 批量操作
    action_list = []

    def get_action_list(self):
        """
        预留钩子：获取批量操作类型
            默认无批量操作功能，可自定义添加，如：
            action_list = [StarkHandler.action_multi_delete, ]
        :return:
        """
        return self.action_list

    def action_multi_delete(self, request, *args, **kwargs):
        """
        批量删除功能
        :return: 删除成功后刷新页面
        """

        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
        return redirect(self.memory_reverse(*args, **kwargs))

    action_multi_delete.text = "批量删除"

    # 添加按钮
    has_add_btn = True

    def get_add_btn(self, request, *args, **kwargs):
        """
        预留钩子之：获取添加按钮
            默认有添加功能
        :return:
        """
        if self.has_add_btn:
            return "<a class='btn btn-success' href='%s'><i class='fa fa-plus' aria-hidden='true'></i>&nbsp;新建</a>" \
                   % self.reverse_add_url(*args, **kwargs)
        return None

    # 分页器：最多展示的页数
    per_page_count = 10

    def get_queryset(self, request, *args, **kwargs):
        """
        预留钩子：
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.model_class.objects

    def list_view(self, request, *args, **kwargs):
        """
        视图函数：列表页面
            附加功能：组合搜索｜关键字搜索｜排序｜批量操作｜数据列表展示｜分页器
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1. 组合搜索
        search_group_row_list = []
        search_group = self.get_search_group()
        for option_object in search_group:
            # 可迭代对象，以渲染html标签
            row = option_object.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
            search_group_row_list.append(row)
        # 组合搜索的搜索条件
        search_group_condition = self.get_search_group_condition(request)

        # 2. 关键字搜索
        search_list = self.get_search_list()
        search_value = request.GET.get('q', '')
        conn = Q()
        conn.connector = 'OR'
        if search_value:
            for item in search_list:
                # 关键字搜索的搜索条件
                conn.children.append((item, search_value))

        # 3. 排序
        order_list = self.get_order_list()

        # 4. 最终数据（组合搜索+关键字搜索+排序）
        prev_queryset = self.get_queryset(request, *args, **kwargs)
        queryset = prev_queryset.filter(conn).filter(**search_group_condition).order_by(*order_list)

        # 5. 数据分页
        all_count = queryset.count()
        query_params = request.GET.copy()
        query_params._mutable = True
        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=self.per_page_count,
        )
        data_list = queryset[pager.start:pager.end]

        # 6.1 数据展示：表格头
        header_list = []
        list_display = self.get_list_display(request, *args, **kwargs)
        if list_display:
            for key_or_func in list_display:
                # 自定义的展示列（包括原生的choice属性）
                if isinstance(key_or_func, FunctionType):
                    verbose_name = key_or_func(self, obj=None, is_header=True)
                # 原生的属性展示列
                else:
                    verbose_name = self.model_class._meta.get_field(key_or_func).verbose_name
                header_list.append(verbose_name)
        else:
            # 没设置展示列时，表头设置为表名
            header_list.append(self.model_class._meta.model_name)
        # 6.2 数据展示：表格内容
        body_list = []
        for row in data_list:
            tr_list = []
            if list_display:
                for key_or_func in list_display:
                    # 自定义的展示列（包括原生的choice属性）
                    if isinstance(key_or_func, FunctionType):
                        tr_list.append(key_or_func(self, row, False, *args, **kwargs))
                    # 原生的属性展示列
                    else:
                        tr_list.append(getattr(row, key_or_func))
            else:
                # 没设置展示列时，表头设置为表的__str__返回值
                tr_list.append(row)
            body_list.append(tr_list)

        # 7.1 批量操作：展示
        action_list = self.get_action_list()
        action_dict = {func.__name__: func.text for func in action_list}
        # 7.2 批量操作：执行
        if request.method == 'POST':
            action_func_name = request.POST.get('action')
            if action_func_name and action_func_name in action_dict:
                action_response = getattr(self, action_func_name)(request, *args, **kwargs)
                # 预留的定制执行成功后的返回页面
                if action_response:
                    return action_response

        # 8. 添加按钮
        add_btn = self.get_add_btn(request, *args, **kwargs)

        return render(
            request,
            self.list_template or 'stark/list.html',
            {
                'header_list': header_list,
                'body_list': body_list,
                'pager': pager,
                'add_btn': add_btn,
                'search_list': search_list,
                'search_value': search_value,
                'action_dict': action_dict,
                'search_group_row_list': search_group_row_list,
            }
        )

    def save(self, request, form, is_update, *args, **kwargs):
        """
        预留钩子：在使用ModelForm保存数据之前预留的钩子方法
            可自定义保存的某个字段的默认值
        :param request:
        :param form: form对象
        :param is_update: 是否是更新操作
        :param args:
        :param kwargs:
        :return:
        """
        form.save()

    def add_view(self, request, *args, **kwargs):
        """
        视图函数：添加页面
        :param request:
        :return:
        """
        model_form_class = self.get_model_form_class(True, request, None, *args, **kwargs)
        if request.method == 'GET':
            form = model_form_class()
            return render(request, self.add_template or 'stark/edit.html', {'form': form})

        form = model_form_class(data=request.POST)
        if form.is_valid():
            response = self.save(request, form, False, *args, **kwargs)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return response or redirect(self.memory_reverse(*args, **kwargs))
        return render(request, self.add_template or 'stark/edit.html', {'form': form})

    def get_edit_object(self, request, pk, *args, **kwargs):
        """
        预留钩子
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        return self.model_class.objects.filter(pk=pk).first()

    def edit_view(self, request, pk, *args, **kwargs):
        """
        视图函数：编辑页面
        :param request:
        :param pk: 要编辑的表的记录id
        :return:
        """
        current_edit_object = self.get_edit_object(request, pk, *args, **kwargs)
        if not current_edit_object:
            return HttpResponse('要修改的数据不存在，请重新选择！')

        model_form_class = self.get_model_form_class(False, request, pk, *args, **kwargs)
        if request.method == 'GET':
            form = model_form_class(instance=current_edit_object)
            return render(request, self.edit_template or 'stark/edit.html', {'form': form})

        form = model_form_class(data=request.POST, instance=current_edit_object)
        if form.is_valid():
            response = self.save(request, form, True, *args, **kwargs)
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return response or redirect(self.memory_reverse(*args, **kwargs))
        return render(request, self.edit_template or 'stark/edit.html', {'form': form})

    def del_object(self, request, pk, *args, **kwargs):
        """
        预留钩子
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        self.model_class.objects.filter(pk=pk).delete()

    def del_view(self, request, pk, *args, **kwargs):
        """
        视图函数：删除页面
        :param request:
        :param pk: 要删除的表的记录id
        :return:
        """
        current_del_object = self.model_class.objects.filter(pk=pk).first()
        if not current_del_object:
            return HttpResponse('要修改的数据不存在，请重新选择！')

        if request.method == 'GET':
            # 确认删除提示页面
            return render(request, self.del_template or 'stark/delete.html',
                          {'cancel': self.memory_reverse(*args, **kwargs)})
        response = self.del_object(request, pk, *args, **kwargs)
        return response or redirect(self.memory_reverse(*args, **kwargs))

    def get_url_name(self, param):
        """
        根据参数获取对应的name别名
        :param param: 参数：'list'、'add'、'edit'、'del'
        :return:
        """
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param,)
        return '%s_%s_%s' % (app_label, model_name, param,)

    @property
    def get_list_url_name(self):
        """
        获取列表页面URL的name
        :return:
        """
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        """
        获取添加页面URL的name
        :return:
        """
        return self.get_url_name('add')

    @property
    def get_edit_url_name(self):
        """
        获取修改页面URL的name
        :return:
        """
        return self.get_url_name('edit')

    @property
    def get_del_url_name(self):
        """
        获取删除页面URL的name
        :return:
        """
        return self.get_url_name('del')

    def reverse_commons_url(self, name, *args, **kwargs):
        """
        生成带有原搜索条件的URL
        :param name: 带参数的原URL
        :param args:
        :param kwargs:
        :return: 带_filter参数的新URL（原参数存在_filter中）
        """
        name = "%s:%s" % (self.site.namespace, name,)
        base_url = reverse(name, args=args, kwargs=kwargs)

        # 当前URL中无参数
        if not self.request.GET:
            new_url = base_url
        # 当前URL中有参数，把参数打包到_filter
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            new_url = "%s?%s" % (base_url, new_query_dict.urlencode())

        return new_url

    def reverse_add_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的添加URL
        :return:
        """
        return self.reverse_commons_url(self.get_add_url_name, *args, **kwargs)

    def reverse_edit_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的编辑URL
        :param pk:
        :return:
        """
        # return self.reverse_commons_url('web_userinfo_edit', pk)
        # return self.reverse_commons_url('web_userinfo_reset_pwd', pk=pk)
        return self.reverse_commons_url(self.get_edit_url_name, *args, **kwargs)

    def reverse_del_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的删除URL
        :param pk:
        :return:
        """
        return self.reverse_commons_url(self.get_url_name('del'), *args, **kwargs)

    def memory_reverse(self, *args, **kwargs):
        """
        自定义反向生成URL
            在URL中将原来搜索条件（_filter后的值，如：/menu/add/?_filter=mid%3D2），reverse生成原来的URL，如：/menu/list/?mid=2
        :return: 带参数的原URL
        """
        name = "%s:%s" % (self.site.namespace, self.get_list_url_name,)
        base_url = reverse(name, args=args, kwargs=kwargs)

        param = self.request.GET.get('_filter')
        if param:
            base_url = "%s?%s" % (base_url, param,)
        return base_url

    def wrapper(self, func):
        """
        为当前对象的request属性值初始化 = request对象
        :param func: 视图函数
        :return: 视图函数
        """

        # 装饰器保留原函数的原信息
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner

    def get_urls(self):
        """
        获取urls文件对象（第二次路由分发）
        :return:
        """
        patterns = [
            url(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            url(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            url(r'^edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), name=self.get_edit_url_name),
            url(r'^del/(?P<pk>\d+)/$', self.wrapper(self.del_view), name=self.get_del_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def extra_urls(self):
        """
        预留钩子：用户自定义除了增删改查，额外需要的url
        :return:
        """
        return []


class StarkSite(object):
    """
    stark注册类
    """
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        """
        注册其他app的models
        :param model_class: ORM映射（其他app的models中的数据库表对应的类，如：models.UserInfo）
        :param handler_class: 核心的类（批量生成对该表增删改查等操作的urls路由和views视图函数）
        :param prev: URL前缀（特别的，如隐私级别较高的项目类，可以按需求在URL中添加一些标识）
        :return:
        """
        if not handler_class:
            handler_class = StarkHandler
        self._registry.append(
            {'model_class': model_class, 'handler': handler_class(self, model_class, prev), 'prev': prev})

    def get_urls(self):
        """
        获取urls文件对象（第一次路由分发）
        :return: urls文件对象
        """
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            # 获取app名、模型名
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            if prev:
                patterns.append(
                    url(
                        r'^%s/%s/%s/' % (app_label, model_name, prev,),
                        (handler.get_urls(), None, None)
                    )
                )
            else:
                patterns.append(
                    url(
                        r'%s/%s/' % (app_label, model_name,),
                        (handler.get_urls(), None, None)
                    )
                )
        return patterns

    @property
    def urls(self):
        """
        获取最终完整的urls路由关系
        :return: (urls文件对象, app别名, app名称空间)
        """
        return self.get_urls(), self.app_name, self.namespace


# 实例化StarkSite类，生成可被其他app公用的site对象
site = StarkSite()
