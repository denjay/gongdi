########################################
# create by :cxh-PC
# create time :2018-02-13 19:22:32.372118
########################################
from app import auth, db, p
from app.models import *
from app.utils import get_login_user,tzstr2datetime
from sqlalchemy.orm import aliased
import os

def docs_get(cls,page = None,per_page = None,buwei = None,doc_name = None,
             shigong_unit=None,jiaodi_ren=None,bei_jiaodi_ren=None) -> str:
    user = get_login_user()
    datap1 = cls.query
    if not user.issystemuser:
        datap1 = datap1.join(Danti, Danti.id == cls.buweiid)
        datap1 = datap1.join(Company_auth,Company_auth.companyid==Danti.companyid)
        datap1 = datap1.filter(Company_auth.appuserid==user.uid)
        if buwei is not None:
            datap1 = datap1.filter(Danti.name.like('%'+'%s'%buwei+'%'))
        if doc_name is not None:
            datap1 = datap1.filter(cls.name.like('%' + '%s' % doc_name + '%'))
        if shigong_unit:
            datap1 = datap1.filter(cls.shigong_unit.like('%' + '%s' % shigong_unit + '%'))
        if jiaodi_ren:
            datap1 = datap1.filter(cls.jiaodi_ren.like('%' + '%s' % jiaodi_ren + '%'))
        if bei_jiaodi_ren:
            datap1 = datap1.filter(cls.bei_jiaodi_ren.like('%' + '%s' % bei_jiaodi_ren + '%'))
    datap2 = cls.query
    if not user.issystemuser:
        dantia = aliased(Danti)
        datap2 =  datap2.join(Buwei,Buwei.id==cls.buweiid)
        datap2 = datap2.join(dantia, dantia.id == Buwei.dantiid)
        datap2 = datap2.join(Company_auth,Company_auth.companyid==dantia.companyid)
        datap2 = datap2.filter(Company_auth.appuserid==user.uid)
        if buwei is not None:
            datap2 = datap2.filter(Buwei.name.like('%'+'%s'%buwei+'%'))
        if doc_name is not None:
            datap2 = datap2.filter(cls.name.like('%' + '%s' % doc_name + '%'))
        if shigong_unit:
            datap2 = datap2.filter(cls.shigong_unit.like('%' + '%s' % shigong_unit + '%'))
        if jiaodi_ren:
            datap2 = datap2.filter(cls.jiaodi_ren.like('%' + '%s' % jiaodi_ren + '%'))
        if bei_jiaodi_ren:
            datap2 = datap2.filter(cls.bei_jiaodi_ren.like('%' + '%s' % bei_jiaodi_ren + '%'))
    datap = datap1.union(datap2).order_by(cls.name).distinct().paginate(page,per_page)
    return [data.to_jsonex() for data in datap.items] ,\
            200 ,{"content-type": "chatset=utf8","x-page":datap.page,"x-total":datap.total}

def docs_post(cls,body) -> str:
    try:
        tzstr2datetime(body,['jiaodi_time'])
        data = cls(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}

def docs_id_get(cls,id) -> str:
    data = cls.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 200, {"content-type": "chatset=utf8"}

def docs_id_put(cls,id,body) -> str:
    try:
        tzstr2datetime(body, ['jiaodi_time'])
        cls.query.filter(cls.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = cls.query.filter_by(id=id).first_or_404()
    return data.to_jsonex(), 201, {"content-type": "chatset=utf8"}

def docs_id_delete(cls,id) -> str:
    q_inspect = cls.query.filter(cls.id == id).first_or_404()
    try:
        for doc_file  in q_inspect.doc_filess:
            db.session.delete(doc_file)
            try:
                os.remove(doc_file.save_file_name)
            except Exception as e:
                pass
        db.session.delete(q_inspect)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
