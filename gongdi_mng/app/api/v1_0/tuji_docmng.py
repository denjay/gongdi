########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:37.000643
########################################
from app import auth, db, p
from app.models import *
from .docmng_utils import docs_get,docs_id_get,docs_id_delete,docs_id_put,docs_post
@auth.valid_login
@p.check("tuji_doc",["view"])
def tuji_docs_get(page = None,per_page = None,buwei = None,doc_name = None,jwt = None) -> str:
    return docs_get(Tuji_doc,page,per_page,buwei,doc_name)
@auth.valid_login
@p.check("tuji_doc",["insert"])
def tuji_docs_post(body,jwt = None) -> str:
    return docs_post(Tuji_doc,body)
@auth.valid_login
@p.check("tuji_doc",["view"])
def tuji_docs_id_get(id,jwt = None) -> str:
    return docs_id_get(Tuji_doc,id)
@auth.valid_login
@p.check("tuji_doc",["edit"])
def tuji_docs_id_put(id,body,jwt = None) -> str:
    return docs_id_put(Tuji_doc,id,body)
@auth.valid_login
@p.check("tuji_doc",["delete"])
def tuji_docs_id_delete(id,jwt = None) -> str:
    return docs_id_delete(Tuji_doc,id)
