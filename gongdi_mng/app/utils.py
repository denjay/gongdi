########################################
# create by :cxh-PC
# create time :2018-01-31 11:55:31.662773
########################################
from flask import g
from collections import namedtuple
from flask import current_app
from mwsdk import Rightmanage
from datetime import datetime
import os
from PIL import Image
from werkzeug.utils import secure_filename
import uuid
User = namedtuple('User', ['uid', 'username', 'issystemuser','ismanageuser','manageuserid'])

def get_file_name(filename,path=None):
    filename_s,ext_name = filename.rsplit('.', 1)
    filename_r = filename_s#secure_filename(filename_s)
    if filename_r:
        filename_new = '%s_%s.%s'%(filename_r,datetime.now().strftime('%y%m%d%H%M%S%f'),ext_name)
    else:
        filename_new =  '%s.%s'%(secure_filename(uuid.uuid4()),ext_name)
    return os.path.join(path,filename_new)

def resize_image(file_name,dpath,width=0,height=0):
    '''
    :param file_name: 图片文件路径名
    :param dpath: 图片文件目标存储路径
    :param width: 目标宽，为0不处理
    :param height: 目标高，为0 不处理
    :return: 目标文件路径
    '''
    def get_rate(ws,wd,hs,hd):
        if ws < wd or hs < hd:
            return 1
        # 调整比率，取最大的比率
        rw = ws / wd
        rh = hs / hd
        return max(rw,rh)
    im = Image.open(file_name)
    if width and height:
        w, h = im.size
        res_rate = get_rate(w,width,h,height)
        # 缩放到设定比率:
        im.thumbnail((round(w / res_rate), round(h / res_rate)))
    # 把缩放后的图像用jpeg格式保存:
    dfile_name = os.path.join(dpath,os.path.split(file_name)[-1])
    im.save(dfile_name, 'jpeg')
    return dfile_name

def str2date(body,dtkeys):
    for key in dtkeys:
        if key in body.keys():
            body[key] = datetime.strptime(body[key], '%Y-%m-%d').date()

def tzstr2datetime(body,dtkeys):
    '''
    置换tzdatetime str 为 datetime
    :param body:dict
    :param dtkeys: 需要转换tzdatetime的keys
    :return:
    '''
    for key in dtkeys:
        if key in body.keys():
            body[key] = datetime.strptime(body[key], '%Y-%m-%dT%H:%M:%S.%fZ')

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
