########################################
# create by :sin
# create time :2018-05-04 09:39:27.397756
########################################
from app import auth, db, p
from app.models import Work_experience
@auth.valid_login
@p.check('work_experience',["view"])
def work_experiences_get(jwt = None):
    datas = Work_experience.query.all()
    return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('work_experience',["view"])
def work_experiences_id_get(id,jwt = None):
    data = Work_experience.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('work_experience',["view"])
def employee_id_work_experiences_get(id,page = None,perpage = None,jwt = None):
    datas = db.session.query(Work_experience).filter(Work_experience.employeeid == id).all()
    return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('work_experience',["delete"])
def work_experiences_id_delete(id,jwt = None):
    try:
        db.session.query(Work_experience).filter(Work_experience.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check('work_experience',["edit"])
def work_experiences_id_put(id,body,jwt = None):
    try:
        Work_experience.query.filter(Work_experience.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Work_experience.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('work_experience',["insert"])
def work_experiences_post(body,jwt = None):
    try:
        # body['id']=new_id
        data = Work_experience(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
