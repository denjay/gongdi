########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.161021
########################################
from app import auth, db, p
from app.models import *
from app.utils import tzstr2datetime,get_login_user
import os
@auth.valid_login
@p.check("emp_illegal",["view"])
def emp_illegals_get(page = None,per_page = None,auditing_status = None,illegal_emp_name = None,illegal_typeid = None,jwt = None):
    user = get_login_user()
    # if user.issystemuser:
    #     datap = Emp_illegal.query. \
    #         order_by(Emp_illegal.illegal_time.desc()).paginate(page, per_page)
    # else:
    datap = Emp_illegal.query
    if not user.issystemuser:
        datap = datap.join(Company_auth, Company_auth.companyid == Emp_illegal.companyid)
        datap = datap.filter(Company_auth.appuserid == user.uid)
    if auditing_status is not None:
        datap = datap.filter(Emp_illegal.auditing_status == auditing_status)
    if illegal_emp_name is not None:
        datap = datap.join(Employee, Employee.id == Emp_illegal.illegal_empid)
        datap = datap.filter(Employee.emp_name.like('%' + '%s' % illegal_emp_name + '%'))
    if illegal_typeid is not None:
        datap = datap.filter(Emp_illegal.illegal_typeid == illegal_typeid)
    datap = datap.order_by(Emp_illegal.illegal_time.desc()).distinct().paginate(page, per_page)
    return [data.to_jsonex() for data in datap.items] ,\
            200 ,{"content-type": "chatset=utf8","x-page":datap.page,"x-total":datap.total}
@auth.valid_login
@p.check("emp_illegal",["insert"])
def emp_illegals_post(body,jwt = None):
    try:
        tzstr2datetime(body,['illegal_time','rectify_time'])
        if body.get('illegal_time') is None:
            body['illegal_time']=datetime.now()
        data = Emp_illegal(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("emp_illegal",["view"])
def emp_illegals_id_get(id,jwt = None):
    data = Emp_illegal.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("emp_illegal",["edit"])
def emp_illegals_id_put(id,body,jwt = None):
    try:
        Emp_illegal.query.filter(Emp_illegal.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Emp_illegal.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("emp_illegal",["delete"])
def emp_illegals_id_delete(id,jwt = None):
    emp_illegal = Emp_illegal.query.filter(Emp_illegal.id == id).first_or_404()
    try:
        for ill_pic  in emp_illegal.illegal_pics:
            db.session.delete(ill_pic)
            try:
                os.remove(ill_pic.save_file_name)
            except Exception as e:
                pass
        db.session.delete(emp_illegal)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
