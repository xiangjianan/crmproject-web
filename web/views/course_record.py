from django.shortcuts import HttpResponse, redirect, render
from django.utils.safestring import mark_safe
from django.urls import reverse, re_path
from django.forms.models import modelformset_factory

from stark.service.stark import StarkHandler, get_datetime_text
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class CourseRecordModelForm(StarkModelForm):
    """
    ModelForm配置：上课记录表
    """

    class Meta:
        model = models.CourseRecord
        fields = ['day_num', 'teacher']


class StudyRecordModelForm(StarkModelForm):
    """
    ModelForm配置：考勤记录表
    """

    class Meta:
        model = models.StudyRecord
        fields = ['record', ]


class CourseRecordHandler(PermissionHandler, StarkHandler):
    """
    stark配置：上课记录表
    """
    # 获取自定义ModelForm
    model_form_class = CourseRecordModelForm

    def display_attendance(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义考勤显示列
        :param obj: 当前上课记录
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '考勤'
        # 当前上课记录所属的课程id
        class_id = obj.class_object.pk
        name = "%s:%s" % (self.site.namespace, self.get_url_name('attendance'),)
        attendance_url = reverse(name, kwargs={'class_id': class_id, 'course_record_id': obj.pk})
        tpl = '<a href="%s">查看</a>' % attendance_url
        return mark_safe(tpl)

    # 页面显示列：复选框｜班级｜节次｜讲师｜时间｜考勤｜自定义编辑删除操作
    list_display = [
        StarkHandler.display_checkbox,
        'class_object', 'day_num', 'teacher',
        get_datetime_text('时间', 'date'),
        display_attendance
    ]

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        钩子方法：自定义编辑删除列
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return mark_safe("""
            <div class="pull-right">
                操作
            </div>""")
        class_id = kwargs.get('class_id')
        tpl = """
            <div class="pull-right">
                <a class="text-primary" style="margin-right: 10px;" href="%s">
                    编辑
                </a>
                <a class="text-danger" href="%s">
                    删除
                </a>
            </div>""" % (self.reverse_edit_url(pk=obj.pk, class_id=class_id),
                         self.reverse_del_url(pk=obj.pk, class_id=class_id))
        return mark_safe(tpl)

    def get_urls(self):
        """
        预留钩子：重写URL
        :return:
        """
        patterns = [
            re_path(r'^list/(?P<class_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<class_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^edit/(?P<class_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.edit_view),
                    name=self.get_edit_url_name),
            re_path(r'^delete/(?P<class_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.del_view),
                    name=self.get_del_url_name),
            re_path(r'^attendance/(?P<class_id>\d+)/(?P<course_record_id>\d+)/$', self.wrapper(self.attendance_view),
                    name=self.get_url_name('attendance')),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        """
        预留钩子：获取当前班级的上课记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        class_id = kwargs.get('class_id')
        return self.model_class.objects.filter(class_object_id=class_id)

    def save(self, request, form, is_update, *args, **kwargs):
        """
        预留钩子：保存前设置默认班级id
        :param request:
        :param form:
        :param is_update:
        :param args:
        :param kwargs:
        :return:
        """
        class_id = kwargs.get('class_id')

        if not is_update:
            form.instance.class_object_id = class_id
        form.save()

    def action_multi_init(self, request, *args, **kwargs):
        """
        批量操作：初始化考勤
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        course_record_id_list = request.POST.getlist('pk')
        class_id = kwargs.get('class_id')
        class_object = models.ClassList.objects.filter(id=class_id).first()
        if not class_object:
            return HttpResponse('班级不存在')
        student_object_list = class_object.student_set.all()

        for course_record_id in course_record_id_list:
            # 判断上课记录是否合法
            course_record_object = models.CourseRecord.objects.filter(id=course_record_id,
                                                                      class_object_id=class_id).first()
            if not course_record_object:
                continue

            # 判断此上课记录的考勤记录是否已经存在
            study_record_exists = models.StudyRecord.objects.filter(course_record=course_record_object).exists()
            if study_record_exists:
                continue

            # 为每个学生在该天创建考勤记录
            study_record_object_list = [models.StudyRecord(student_id=stu.id, course_record_id=course_record_id) for stu
                                        in student_object_list]
            # 批量导入
            models.StudyRecord.objects.bulk_create(study_record_object_list, batch_size=50)

        return redirect(self.memory_reverse(*args, **kwargs))

    action_multi_init.text = '批量初始化考勤'

    # 允许的批量操作：初始化考勤
    action_list = [action_multi_init, ]

    def attendance_view(self, request, class_id, course_record_id, *args, **kwargs):
        """
        视图函数：考勤的批量操作
        :param request:
        :param class_id:
        :param course_record_id:
        :param args:
        :param kwargs:
        :return:
        """
        # 当前上课记录的所有考勤
        study_record_object_list = models.StudyRecord.objects.filter(course_record_id=course_record_id)
        # 考勤表formset
        study_model_formset = modelformset_factory(models.StudyRecord, form=StudyRecordModelForm, extra=0)

        if request.method == 'POST':
            formset = study_model_formset(queryset=study_record_object_list, data=request.POST)
            if formset.is_valid():
                formset.save()
                return redirect(self.memory_reverse(*args, **{'class_id': class_id}))
            return render(request, 'attendance.html', {'formset': formset})

        formset = study_model_formset(queryset=study_record_object_list)
        return render(request, 'attendance.html', {'formset': formset})
