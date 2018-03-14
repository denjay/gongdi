########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:36.540229
########################################
from app import auth, qrcode, p
from app.models import *
from flask import send_file
@auth.valid_login
@p.check("danti",["insert"])
def dantis_post(body,jwt = None) -> str:
    print('dfgdgdgdgdfgfggdgsdgeef==============================')
    try:
        data = Danti(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("danti",["view"])
def dantis_id_get(id,jwt = None) -> str:
    data = Danti.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("danti",["edit"])
def dantis_id_put(id,body,jwt = None) -> str:
    try:
        Danti.query.filter(Danti.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Danti.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("danti",["delete"])
def dantis_id_delete(id,jwt = None) -> str:
    try:
        db.session.query(Danti).filter(Danti.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check("danti",["view"])
def company_id_dantis_get(id,page = None,per_page = None,jwt = None) -> str:
    datap = Danti.query.\
        filter(Danti.companyid==id).\
        order_by(Danti.name).paginate(page,per_page)
    return [data.to_jsonex() for data in datap.items] ,\
            200 ,{"content-type": "chatset=utf8","x-page":datap.page,"x-total":datap.total}
def danti_qrcode_id_get(id,jwt = None) -> str:
    try:
        return send_file(qrcode('/links/danti/%s/detail'%id, mode='raw'),
                         mimetype='image/png')
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
