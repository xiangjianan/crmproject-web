"""
自定义加密模块
"""
import hashlib


def gen_md5(origin):
    """
    md5加密
    :param origin:
    :return:
    """
    # 密码加盐
    ha = hashlib.md5(b'jk3usodfjwkrsdf')
    ha.update(origin.encode('utf-8'))
    return ha.hexdigest()
