from app.models import *
from app.utils import get_login_user,str2date
from datetime import datetime
from sqlalchemy.orm import aliased
import os

def inspect_cls_get(cls,page = None,per_page = None,insp_emp = None,insp_date = None,buwei = None,buweiid=None) -> str:
    user = get_login_user()
    dantia = aliased(Danti)
    datap = cls.query
    if not user.issystemuser:
        datap =  datap.join(Buwei,Buwei.id==cls.buweiid)
        datap = datap.join(dantia, dantia.id == Buwei.dantiid)
        datap = datap.join(Company_auth,Company_auth.companyid==dantia.companyid)
        datap = datap.filter(Company_auth.appuserid==user.uid)
        if buwei is not None:
            datap = datap.filter(Buwei.name.like('%'+'%s'%buwei+'%'))
    if buweiid is not None:
        datap = datap.filter(cls.buweiid==buweiid)
    if insp_emp is not None:
        datap = datap.filter(cls.insp_emp.like('%'+'%s'%insp_emp+'%'))
    if insp_date is not None:
        insp_date = datetime.strptime(insp_date,'%Y-%m-%d').date()
        datap = datap.filter(cls.insp_date==insp_date)
    datap = datap.order_by(cls.insp_date.desc()).distinct()
    headers = {"content-type": "chatset=utf8"}
    if page and per_page:
        datap = datap.paginate(page,per_page)
        datas = datap.items
        headers.update({"x-page":datap.page,"x-total":datap.total})
    else:
        datas = datap.all()
    return [data.to_jsonex() for data in datas] ,\
            200 ,headers

def inspect_cls_post(cls,body) -> str:
    try:
        str2date(body,['insp_date'])
        data = cls(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}

def inspect_cls_id_get(cls,id) -> str:
    data = cls.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 200, {"content-type": "chatset=utf8"}

def inspect_cls_id_put(cls,id,body) -> str:
    try:
        str2date(body, ['insp_date'])
        cls.query.filter(cls.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = cls.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}

def inspect_cls_id_delete(cls,id) -> str:
    q_inspect = cls.query.filter(cls.id == id).first_or_404()
    try:
        for insp_pic  in q_inspect.inspect_pics:
            db.session.delete(insp_pic)
            try:
                os.remove(insp_pic.save_file_name)
            except Exception as e:
                pass
        db.session.delete(q_inspect)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
