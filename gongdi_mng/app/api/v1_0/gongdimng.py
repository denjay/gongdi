########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:36.765429
########################################
from app import auth, qrcode, p
from app.models import *
from app.utils import str2date
from flask import send_file
@auth.valid_login
@p.check("gongdi",["insert"])
def gongdis_post(body,jwt = None) -> str:
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
def gongdis_id_get(id,jwt = None) -> str:
    data = Gongdi.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("gongdi",["edit"])
def gongdis_id_put(id,body,jwt = None) -> str:
    try:
        Gongdi.query.filter(Gongdi.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Gongdi.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("gongdi",["delete"])
def gongdis_id_delete(id,jwt = None) -> str:
    try:
        db.session.query(Gongdi).filter(Gongdi.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check("gongdi",["view"])
def companys_comp_id_gongdis_get(comp_id,jwt = None) -> str:
    data = Gongdi.query.filter_by(companyid=comp_id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
def gongdis_qrcode_id_get(id,jwt = None) -> str:
    try:
        return send_file(qrcode('/gongdis/%s'%id, mode='raw'),
                         mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
