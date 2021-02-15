from django.utils.safestring import mark_safe
from django.urls import reverse

from stark.service.stark import StarkHandler, get_datetime_text, get_m2m_text, Option
from stark.forms.widgets import DateTimePickerInput
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class ClassListModelForm(StarkModelForm):
    """
    ModelForm配置：班级表
    """

    class Meta:
        model = models.ClassList
        fields = '__all__'
        # 自定义forms表单的显示形式
        widgets = {
            'start_date': DateTimePickerInput,
            'graduate_date': DateTimePickerInput,
        }


class ClassListHandler(PermissionHandler, StarkHandler):
    """
    stark配置：班级表
    """
    # 获取自定义ModelForm
    model_form_class = ClassListModelForm

    def display_course(self, obj=None, is_header=None):
        """
        自定义的班级的显示列
        :param obj: 当前记录对象
        :param is_header: 是否是表头
        :return:
        """
        if is_header:
            return '班级'
        return "%s（%s期）" % (obj.course.name, obj.semester,)

    def display_course_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义的上课记录显示列
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '上课记录'
        record_url = reverse('stark:web_courserecord_list', kwargs={'class_id': obj.pk})
        return mark_safe('<a href="%s">查看</a>' % record_url)

    # 页面显示列：校区｜班级｜学费｜开班日期｜班主任｜任课老师｜上课记录
    list_display = [
        'school', display_course, 'price',
        get_datetime_text('开班日期', 'start_date'),
        'class_teacher',
        get_m2m_text('任课老师', 'tech_teachers'),
    ]

    def get_list_display(self, request, *args, **kwargs):
        """
        预留钩子：增加自定义的上课记录显示列
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_course_record)
        return value

    # 允许的组合搜索条件：学校｜课程
    search_group = [
        Option('school'),
        Option('course'),
    ]
