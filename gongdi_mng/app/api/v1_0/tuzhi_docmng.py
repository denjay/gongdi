########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:36.947595
########################################
from app import auth, db, p
from app.models import *
from .docmng_utils import docs_get,docs_id_get,docs_id_delete,docs_id_put,docs_post
@auth.valid_login
@p.check("tuzhi_doc",["view"])
def tuzhi_docs_get(page = None,per_page = None,buwei = None,doc_name = None,jwt = None) -> str:
    return docs_get(Tuzhi_doc, page, per_page, buwei, doc_name)
@auth.valid_login
@p.check("tuzhi_doc",["insert"])
def tuzhi_docs_post(body,jwt = None) -> str:
    return docs_post(Tuzhi_doc,body)
@auth.valid_login
@p.check("tuzhi_doc",["view"])
def tuzhi_docs_id_get(id,jwt = None) -> str:
    return docs_id_get(Tuzhi_doc,id)
@auth.valid_login
@p.check("tuzhi_doc",["edit"])
def tuzhi_docs_id_put(id,body,jwt = None) -> str:
    return docs_id_put(Tuzhi_doc,id,body)
@auth.valid_login
@p.check("tuzhi_doc",["delete"])
def tuzhi_docs_id_delete(id,jwt = None) -> str:
    return docs_id_delete(Tuzhi_doc,id)
