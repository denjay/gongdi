########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.223503
########################################
from app import auth, db, p
from app.models import *
from .inspectmng_utils import inspect_cls_get,inspect_cls_id_get,inspect_cls_id_put,\
                              inspect_cls_id_delete,inspect_cls_post
@auth.valid_login
@p.check("produce_inspect",["view"])
def produce_inspects_get(page = None,per_page = None,insp_emp = None,insp_date = None,buwei = None,buweiid = None,jwt = None):
    return inspect_cls_get(Produce_inspect,page,per_page,insp_emp,insp_date,buwei,buweiid)
@auth.valid_login
@p.check("produce_inspect",["insert"])
def produce_inspects_post(body,jwt = None):
    return inspect_cls_post(Produce_inspect,body)
@auth.valid_login
@p.check("produce_inspect",["view"])
def produce_inspects_id_get(id,jwt = None):
    return inspect_cls_id_get(Produce_inspect,id)
@auth.valid_login
@p.check("produce_inspect",["edit"])
def produce_inspects_id_put(id,body,jwt = None):
    return inspect_cls_id_put(Produce_inspect,id,body)
@auth.valid_login
@p.check("produce_inspect",["delete"])
def produce_inspects_id_delete(id,jwt = None):
    return inspect_cls_id_delete(Produce_inspect,id)
