########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:36.105836
########################################
from app import auth, db, p
from app.models import *
from app.utils import str2date,get_login_user
@auth.valid_login
@p.check("subcontractor",["view"])
def subcontractors_get(page = None,per_page = None,comp_name = None,manager = None,jwt = None) -> str:
    user = get_login_user()
    if user.issystemuser:
        datap = Subcontractor.query.order_by(Subcontractor.comp_name).paginate(page,per_page)
    else:
        datap = Subcontractor.query
        datap = datap.join(Company_auth, Company_auth.companyid == Subcontractor.companyid)
        datap = datap.filter(Company_auth.appuserid ==user.uid)
        if comp_name is not None:
            datap = datap.filter(Subcontractor.comp_name.like('%' + '%s' % comp_name + '%'))
        if manager is not None:
            datap = datap.filter(Subcontractor.manager.like('%' + '%s' % manager + '%'))
        datap = datap.order_by(Subcontractor.comp_name).distinct().paginate(page, per_page)
    return [data.to_json() for data in datap.items] ,\
            200 ,{"content-type": "chatset=utf8","x-page":datap.page,"x-total":datap.total}
@auth.valid_login
@p.check("subcontractor",["insert"])
def subcontractors_post(body,jwt = None) -> str:
    try:
        str2date(body,['approach_date','departure_date'])
        data = Subcontractor(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("subcontractor",["view"])
def subcontractors_id_get(id,jwt = None) -> str:
    data = Subcontractor.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("subcontractor",["edit"])
def subcontractors_id_put(id,body,jwt = None) -> str:
    try:
        Subcontractor.query.filter(Subcontractor.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Subcontractor.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("subcontractor",["delete"])
def subcontractors_id_delete(id,jwt = None) -> str:
    try:
        db.session.query(Subcontractor).filter(Subcontractor.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
