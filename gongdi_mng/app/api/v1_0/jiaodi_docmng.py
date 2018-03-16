########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:37.040678
########################################
from app import auth, db, p
from app.models import *
from .docmng_utils import docs_get,docs_id_get,docs_id_delete,docs_id_put,docs_post
@auth.valid_login
@p.check("jiaodi_doc",["view"])
def jiaodi_docs_get(page = None,per_page = None,buwei = None,shigong_unit = None,jiaodi_ren = None,bei_jiaodi_ren = None,jwt = None) -> str:
    return docs_get(Jiaodi_doc,page,per_page,buwei=buwei,
                    shigong_unit=shigong_unit,jiaodi_ren=jiaodi_ren,
                    bei_jiaodi_ren=bei_jiaodi_ren)
@auth.valid_login
@p.check("jiaodi_doc",["insert"])
def jiaodi_docs_post(body,jwt = None) -> str:
    return docs_post(Jiaodi_doc,body)
@auth.valid_login
@p.check("jiaodi_doc",["view"])
def jiaodi_docs_id_get(id,jwt = None) -> str:
    return docs_id_get(Jiaodi_doc,id)
@auth.valid_login
@p.check("jiaodi_doc",["edit"])
def jiaodi_docs_id_put(id,body,jwt = None) -> str:
    return docs_id_put(Jiaodi_doc,id,body)
@auth.valid_login
@p.check("jiaodi_doc",["delete"])
def jiaodi_docs_id_delete(id,jwt = None) -> str:
    return docs_id_delete(Jiaodi_doc,id)
