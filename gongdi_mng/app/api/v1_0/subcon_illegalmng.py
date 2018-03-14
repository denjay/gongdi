########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:35.845599
########################################
from app import auth, db, p
from app.models import *
from app.utils import tzstr2datetime
from app.utils import get_login_user
from flask import g
import os
@auth.valid_login
@p.check("subcon_illegal",["view"])
def subcon_illegals_get(page = None,per_page = None,auditing_status = None,subcon_name = None,illegal_typeid = None,jwt = None) -> str:
    user = get_login_user()
    if user.issystemuser:
        datap = Subcon_illegal.query. \
            order_by(Subcon_illegal.illegal_time.desc()).paginate(page, per_page)
    else:
        datap = Subcon_illegal.query
        datap = datap.join(Company_auth, Company_auth.companyid == Subcon_illegal.companyid)
        datap = datap.filter(Company_auth.appuserid ==user.uid)
        if auditing_status is not None:
            datap = datap.filter(Subcon_illegal.auditing_status==auditing_status)
        if subcon_name is not None:
            datap = datap.join(Subcontractor,Subcontractor.id==Subcon_illegal.subcontractorid)
            datap = datap.filter(Subcontractor.comp_name.like('%'+'%s'%subcon_name+'%'))
        if illegal_typeid is not None:
            datap = datap.filter(Subcon_illegal.illegal_typeid==illegal_typeid)
        datap = datap.order_by(Subcon_illegal.illegal_time.desc()).distinct().paginate(page, per_page)
    return [data.to_jsonex() for data in datap.items] ,\
            200 ,{"content-type": "chatset=utf8","x-page":datap.page,"x-total":datap.total}
@auth.valid_login
@p.check("subcon_illegal",["insert"])
def subcon_illegals_post(body,jwt = None) -> str:
    try:
        tzstr2datetime(body,['rectify_time','illegal_time'])
        if body.get('illegal_time') is None:
            body['illegal_time']=datetime.now()
        illegal_emp = Employee.query.filter(Employee.login_user==g.user_name).first()
        data = Subcon_illegal(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("subcon_illegal",["view"])
def subcon_illegals_id_get(id,jwt = None) -> str:
    data = Subcon_illegal.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("subcon_illegal",["edit"])
def subcon_illegals_id_put(id,body,jwt = None) -> str:
    try:
        Subcon_illegal.query.filter(Subcon_illegal.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Subcon_illegal.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("subcon_illegal",["delete"])
def subcon_illegals_id_delete(id,jwt = None) -> str:
    subcon_illegal = Subcon_illegal.query.filter(Subcon_illegal.id == id).first_or_404()
    try:
        for ill_pic  in subcon_illegal.illegal_pics:
            db.session.delete(ill_pic)
            try:
                os.remove(ill_pic.save_file_name)
            except Exception as e:
                pass
        db.session.delete(subcon_illegal)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
