from stark.service.stark import StarkHandler
from .base import PermissionHandler


class CourseHandler(PermissionHandler, StarkHandler):
    """
    stark配置：课程表
    """
    # 页面显示列：课程名称｜默认编辑删除操作
    list_display = [
        'name',
    ]

