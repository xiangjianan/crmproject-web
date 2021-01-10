from stark.service.stark import StarkHandler

from .base import PermissionHandler


class SchoolHandler(PermissionHandler, StarkHandler):
    """
    stark配置：学校表
    """
    # 页面显示列：校区名称｜默认编辑删除操作
    list_display = [
        'title',
    ]
