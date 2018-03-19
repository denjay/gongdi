########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.254755
########################################
import time
from app import auth, qrcode, p
from app.models import *
from app.utils import str2date
from flask import send_file
@auth.valid_login
@p.check("gongdi",["insert"])
def gongdis_post(body,jwt = None):
    # 将字符串转为python格式date
    if body['starttime']:
        starttime = body['starttime']
        time_struct = time.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%fZ')
        time_stamp = time.mktime(time_struct) - time.altzone
        time_str_local = time.strftime('%Y-%m-%d', time.localtime(time_stamp))
        body['starttime'] = time_str_local
    else:
        body.pop('starttime')

    if body['complete_time']:
        complete_time = body['complete_time']
        time_struct = time.strptime(complete_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        time_stamp = time.mktime(time_struct) - time.altzone
        time_str_local = time.strftime('%Y-%m-%d', time.localtime(time_stamp))
        body['complete_time'] = time_str_local
    else:
        body.pop('complete_time')

    try:
        str2date(body,['complete_time','starttime'])
        data = Gongdi(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("gongdi",["view"])
def gongdis_id_get(id,jwt = None):
    data = Gongdi.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("gongdi",["edit"])
def gongdis_id_put(id,body,jwt = None):
    # 将字符串转为python格式date
    if body['starttime']:
        starttime = body['starttime']
        if 'T' in starttime:
            time_struct = time.strptime(starttime, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            time_struct = time.strptime(starttime, '%Y-%m-%d')
        time_stamp = time.mktime(time_struct) - time.altzone
        time_str_local = time.strftime('%Y-%m-%d', time.localtime(time_stamp))
        body['starttime'] = time_str_local
        str2date(body, ['starttime'])
    else:
        body['starttime'] = None

    if body['complete_time']:
        complete_time = body['complete_time']
        if 'T' in complete_time:
            time_struct = time.strptime(complete_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            time_struct = time.strptime(complete_time, '%Y-%m-%d')
        time_stamp = time.mktime(time_struct) - time.altzone
        time_str_local = time.strftime('%Y-%m-%d', time.localtime(time_stamp))
        body['complete_time'] = time_str_local
        str2date(body, ['complete_time'])
    else:
        body['complete_time'] = None

    try:
        Gongdi.query.filter(Gongdi.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Gongdi.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("gongdi",["delete"])
def gongdis_id_delete(id,jwt = None):
    try:
        db.session.query(Gongdi).filter(Gongdi.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check("gongdi",["view"])
def companys_comp_id_gongdis_get(comp_id,jwt = None):
    data = Gongdi.query.filter_by(companyid=comp_id).first()
    if data:
        return data.to_json(), 200, {"content-type": "chatset=utf8"}
    else:
        return None
@auth.valid_login
def gongdis_qrcode_id_get(id,jwt = None):
    try:
        return send_file(qrcode('/gongdis/%s'%id, mode='raw'),
                         mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
