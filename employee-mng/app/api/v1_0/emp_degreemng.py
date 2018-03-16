########################################
# create by :cxh-pc
# create time :2018-03-15 18:39:26.902711
########################################
from app import auth, db, p
from app.models import Emp_degree
@auth.valid_login
@p.check('emp_degree',["view"])
def emp_degreess_get(jwt = None):
    datas = Emp_degree.query.all()
    return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('emp_degree',["view"])
def emp_degreess_id_get(id,jwt = None):
    data = Emp_degree.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('emp_degree',["view"])
def employee_id_emp_degreess_get(id,page = None,perpage = None,jwt = None):
    datas = db.session.query(Emp_degree).filter(Emp_degree.employeeid == id).all()
    return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('emp_degree',["delete"])
def emp_degreess_id_delete(id,jwt = None):
    try:
        db.session.query(Emp_degree).filter(Emp_degree.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check('emp_degree',["edit"])
def emp_degreess_id_put(id,body,jwt = None):
    try:
        Emp_degree.query.filter(Emp_degree.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Emp_degree.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('emp_degree',["insert"])
def emp_degreess_post(body,jwt = None):
    try:
        # body['id']=new_id
        data = Emp_degree(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
def emp_degreess_id_del(id) -> str:
    result = {"employeeid": "integer", "id": "integer", "school_name": "string", "department": "string", "study_begin": "date", "study_end": "date", "degree_type": "string", "remark": "string", "degree_name": "string"}
    return result,200,{'content-type': 'chatset=utf8'}
