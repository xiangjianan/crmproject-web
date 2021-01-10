from stark.service.stark import StarkHandler

from .base import PermissionHandler


class DepartmentHandler(PermissionHandler, StarkHandler):
    """
    stark配置：部门表
    """
    # 页面显示列：部门名称｜默认编辑删除操作
    list_display = [
        'title',
    ]
