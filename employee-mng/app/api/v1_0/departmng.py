########################################
# create by :cxh-pc
# create time :2018-03-15 18:39:26.880696
########################################
from app import auth, db, p
from app.models import Depart,Company,Company_auth,Employee
from app.utils import get_login_user
@auth.valid_login
@p.check('depart',["view"])
def departs_get(jwt = None):
    user = get_login_user()
    if user.issystemuser:
        datas = Depart.query.all()
    else:
        # datas_q1 = Depart.query.join(Company, Company.id == Depart.companyid).\
        #     join(Employee, Employee.departid == Depart.id). \
        #     filter(Employee.login_user == user.username)
        datas_q2 = Depart.query.join(Company, Company.id == Depart.companyid). \
            join(Company_auth, Company_auth.companyid == Company.id). \
            filter(Company_auth.appuserid == user.uid)
        datas = datas_q2.distinct().all()
    return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('depart',["view"])
def departs_id_get(id,jwt = None):
    data = Depart.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
# @auth.valid_login
# def departs_id_delete(body) -> str:
#     try:
#         id = body.get('id')
#         db.session.query(Depart).filter(Depart.id == id).delete()
#     except Exception as e:
#         db.session.rollback()
#         return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
#     return {"id": id}, 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('depart',["delete"])
def departs_id_delete(id,jwt = None):
    try:
        db.session.query(Depart).filter(Depart.id == id).delete()
        for item in db.session.query(Depart).filter(Depart.inside_id.like('%-' + str(id) + '-%')):
            db.session.query(Depart).filter(Depart.id == item.id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check('depart',["edit"])
def departs_id_put(id,body,jwt = None):
    try:
        # id = body.get('id')
        # del body['id']
        Depart.query.filter(Depart.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Depart.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('depart',["insert"])
def departs_post(body,jwt = None):
    try:
        if 'parentId' in body:
            body.pop('parentId')
        if 'id' in body:
            body.pop('id')
        data = Depart(**body)
        '''
        if(data.inside_id):
            data.inside_id = data.inside_id + ('_')
        '''
        db.session.add(data)
        db.session.commit()
        '''
        if(data.inside_id):
            data.inside_id=data.inside_id+str(data.id)
        else:
            data.inside_id = str(data.id)
        Depart.query.filter(Depart.id == data.id).update(data.to_json())
        db.session.commit()
        '''
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return {"data": data.to_json()}, 201, {"content-type": "chatset=utf8"}
def get_company_id_departs_get(id):
    datas = Depart.query.filter_by(companyid=id).all()
    return datas
@auth.valid_login
def company_id_departs_lk_get(id,jwt = None):
    result = get_company_id_departs_get(id)
    return [data.to_json() for data in result], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('depart',["view"])
def company_id_departs_get(id,jwt = None):
    result = get_company_id_departs_get(id)
    return [data.to_json() for data in result], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
def depart_trees_get(c_id):
    datas = Depart.query.filter_by(companyid=c_id).all()
    id_map = {}
    for d in datas:
        id_map[d.id]=d
    result = []
    # company = Company.query.filter_by(id=c_id).first()
    for d in datas:
        inside_id = d.inside_id
        parent_ids = inside_id.split('-')[:-1]
        parent_names = []
        for id in parent_ids:
            if id=='':
                continue
            parent_names.append(id_map[int(id)].depart_name)
        parent_names.append(d.depart_name)
        result.append({'d_name':'/'.join(parent_names),
                       'id':d.id,
                       'inside_id':d.inside_id})
    return result,200,{'content-type': 'chatset=utf8'}
