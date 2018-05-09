########################################
# create by :sin
# create time :2018-05-04 09:39:27.372690
########################################
from app import auth, db, p
from app.models import Company_auth,Company,new_id
from app.utils import get_login_user
@auth.valid_login
@p.check('companyauth',["view"])
def company_auths_get(jwt = None):
    try:
        user = get_login_user()
        if user.issystemuser:
            datas = Company_auth.query.all()
            return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
        else:
            datas=db.session.query(Company_auth).\
                filter(Company_auth.appuserid==user.uid).all()
            return [data.to_json() for data in datas], 200, {'content-type': 'chatset=utf8'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('companyauth',["view"])
def company_auths_id_get(id,jwt = None):
    data = Company_auth.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('company',["view"])
def employeename_company_get(jwt = None):
    try:
        user = get_login_user()
        if user.issystemuser:
            datas = Company.query.all()
            return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
        else:
            datas = db.session.query(Company.id,Company.company_code,Company.company_name,Company.remark,Company.companyid).\
                join(Company_auth,Company_auth.companyid==Company.id).\
                filter(Company_auth.appuserid==user.uid).all()
            return [data.to_json() for data in datas], 200, {'content-type': 'chatset=utf8'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('companyauth',["delete"])
def company_auths_id_delete(id,jwt = None):
    try:
        data = Company_auth.query.filter_by(id=id).first_or_404()
        db.session.query(Company_auth).filter(Company_auth.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data, 204, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('companyauth',["edit"])
def company_auths_id_put(id,body,jwt = None):
    try:
        Company_auth.query.filter(Company_auth.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Company_auth.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('companyauth',["insert"])
def company_auths_post(body,jwt = None):
    try:
        companyids = body['companyid'].split(',')
        datas=[]
        for items in companyids:
            body['companyid']=int(items)
            body['id']=new_id()
            data = Company_auth(**body)
            datas.append(data)
            db.session.add(data)
            db.session.commit()
        if datas !=[]:
            return [data.to_json() for data in datas], 201, {"content-type": "chatset=utf8"}
        else:
            return [{"success": "success"}],201,{"content-type": "chatset=utf8"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
# @auth.valid_login
# @p.check('companyauth',["delete"])
# def delete_auth(id) -> str:
#     user = get_login_user()
#     try:
#         data = Company_auth.query.filter_by(id=id).first_or_404()
#         if data is not None:
#             com = Company.query.filter(Company.create_userid==user.uid).first()
#             if com:
#
#         db.session.query(Company_auth).filter(Company_auth.id == id).delete()
#     except Exception as e:
#         db.session.rollback()
#         return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
#     return data, 204, {"content-type": "chatset=utf8"}
def empid_companyauth_get(id,jwt = None):
    try:
        datas = db.session.query(Company_auth). \
            filter(Company_auth.appuserid == id).all()
        return [data.to_json() for data in datas], 200, {'content-type': 'chatset=utf8'}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
