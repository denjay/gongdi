########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:36.321030
########################################
from app import auth, db, p
from app.models import *
from .inspectmng_utils import inspect_cls_get,inspect_cls_id_get,inspect_cls_id_put,\
                              inspect_cls_id_delete,inspect_cls_post
@auth.valid_login
@p.check("safety_inspect",["view"])
def safety_inspects_get(page = None,per_page = None,insp_emp = None,insp_date = None,buwei = None,buweiid = None,jwt = None) -> str:
    return inspect_cls_get(Safety_inspect,page,per_page,insp_emp,insp_date,buwei,buweiid)
@auth.valid_login
@p.check("safety_inspect",["insert"])
def safety_inspects_post(body,jwt = None) -> str:
    return inspect_cls_post(Safety_inspect,body)
@auth.valid_login
@p.check("safety_inspect",["view"])
def safety_inspects_id_get(id,jwt = None) -> str:
    return inspect_cls_id_get(Safety_inspect,id)
@auth.valid_login
@p.check("safety_inspect",["edit"])
def safety_inspects_id_put(id,body,jwt = None) -> str:
    return inspect_cls_id_put(Safety_inspect,id,body)
@auth.valid_login
@p.check("safety_inspect",["delete"])
def safety_inspects_id_delete(id,jwt = None) -> str:
    return inspect_cls_id_delete(Safety_inspect,id)
