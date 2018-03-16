########################################
# create by :cxh-PC
# create time :2017-12-13 20:05:40.976906
########################################
########################################
# create by :cxh-PC
# create time :2017-12-01 19:09:45.427250
########################################
from flask import g
from collections import namedtuple
from flask import current_app
from mwsdk import Rightmanage
User = namedtuple('User', ['uid', 'username', 'issystemuser','ismanageuser','manageuserid'])
def get_login_user():
    '''
    如果是开发模式，直接返回config中设定的结果
    :return: 登录用户信息
    '''
    if current_app.config.get('DEVELOPMENT', False):
        return User(uid=current_app.config.get('LOGIN_USER_ID'),
                    username=current_app.config.get('LOGIN_USER_NAME'),
                    issystemuser=current_app.config.get('LOGIN_USER_SYSTEMUSER',True),
                    ismanageuser=current_app.config.get('LOGIN_USER_MANAGEUSER',False),
                    manageuserid=current_app.config.get('LOGIN_USER_MANAGEUSER_ID','')
                    )
    _, user_js = Rightmanage().cur_user(g.jwt)
    return User(uid=user_js['uid'],
                username=user_js['uname'],
                issystemuser=user_js['systemuser'],
                ismanageuser=user_js['manageuser'],
                manageuserid=user_js['manageuserid']
                )
def p_check(system,subsystem,actions,msg=''):
    '''
    检查是否有权限，代码范例
    p_check(p.sys, 'expense_account', ['reauditing'],'没有反审核账目的权限！')
    '''
    if current_app.config.get('DEVELOPMENT', False):
        return
    _,permissions_js = Rightmanage().cur_permissions(system,g.jwt)
    permission = permissions_js.get(subsystem)
    if permission is None:
        raise Exception('the subsystem(%s) is not exist' % subsystem)
    ops = permission.get('ops')
    if not [act for act in actions if act in ops]:
        if not msg:
            msg = 'The user(%s) have no this (%s) right!'%(g.user_name,ops)
        raise Exception(msg)
