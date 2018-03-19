########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.207880
########################################
from app import auth, db, p
from app.models import *
from .inspectmng_utils import inspect_cls_get,inspect_cls_id_get,inspect_cls_id_put,\
                              inspect_cls_id_delete,inspect_cls_post
@auth.valid_login
@p.check("quality_inspect",["view"])
def quality_inspects_get(page = None,per_page = None,insp_emp = None,insp_date = None,buwei = None,buweiid = None,jwt = None):
    return inspect_cls_get(Quality_inspect,page,per_page,insp_emp,insp_date,buwei,buweiid)
@auth.valid_login
@p.check("quality_inspect",["insert"])
def quality_inspects_post(body,jwt = None):
    return inspect_cls_post(Quality_inspect,body)
@auth.valid_login
@p.check("quality_inspect",["view"])
def quality_inspects_id_get(id,jwt = None):
    return inspect_cls_id_get(Quality_inspect,id)
@auth.valid_login
@p.check("quality_inspect",["edit"])
def quality_inspects_id_put(id,body,jwt = None):
    return inspect_cls_id_put(Quality_inspect,id,body)
@auth.valid_login
@p.check("quality_inspect",["delete"])
def quality_inspects_id_delete(id,jwt = None):
    return inspect_cls_id_delete(Quality_inspect,id)
