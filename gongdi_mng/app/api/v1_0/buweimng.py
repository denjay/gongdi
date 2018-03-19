########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.239128
########################################
from app import auth, qrcode, p
from app.models import *
from flask import send_file
@auth.valid_login
@p.check("buwei",["insert"])
def buweis_post(body,jwt = None):
    try:
        data = Buwei(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("buwei",["view"])
def buweis_id_get(id,jwt = None):
    data = Buwei.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("buwei",["edit"])
def buweis_id_put(id,body,jwt = None):
    try:
        Buwei.query.filter(Buwei.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Buwei.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("buwei",["delete"])
def buweis_id_delete(id,jwt = None):
    try:
        db.session.query(Buwei).filter(Buwei.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check("buwei",["view"])
def dantis_id_buweis_get(id,page = None,per_page = None,jwt = None):
    datap = Buwei.query.filter(Buwei.dantiid==id).order_by(Buwei.name).paginate(page,per_page)
    return [data.to_jsonex() for data in datap.items] ,\
            200 ,{"content-type": "chatset=utf8","x-page":datap.page,"x-total":datap.total}
@auth.valid_login
def bw_jishu_qrcode_id_get(id,jwt = None):
    try:
        return send_file(qrcode('/links/doc-jishus/%s'%id, mode='raw'),
                         mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
def bw_quality_qrcode_id_get(id,jwt = None):
    try:
        return send_file(qrcode('/links/quality/inspects/%s'%id, mode='raw'),
                         mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
def bw_safety_qrcode_id_get(id,jwt = None):
    try:
        return send_file(qrcode('/links/safety/inspects/%s'%id, mode='raw'),
                         mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
def bw_produce_qrcode_id_get(id,jwt = None):
    try:
        return send_file(qrcode('/links/produce/inspects/%s'%id, mode='raw'),
                         mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
