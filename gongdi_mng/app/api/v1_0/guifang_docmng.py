########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.270382
########################################
from app import auth, db, p
from app.models import *
from .docmng_utils import docs_get,docs_id_get,docs_id_delete,docs_id_put,docs_post
@auth.valid_login
@p.check("guifang_doc",["view"])
def guifang_docs_get(page = None,per_page = None,buwei = None,doc_name = None,jwt = None):
    return docs_get(Guifang_doc,page,per_page,buwei,doc_name)
@auth.valid_login
@p.check("guifang_doc",["insert"])
def guifang_docs_post(body,jwt = None):
    return docs_post(Guifang_doc,body)
@auth.valid_login
@p.check("guifang_doc",["view"])
def guifang_docs_id_get(id,jwt = None):
    return docs_id_get(Guifang_doc,id)
@auth.valid_login
@p.check("guifang_doc",["edit"])
def guifang_docs_id_put(id,body,jwt = None):
    return docs_id_put(Guifang_doc,id,body)
@auth.valid_login
@p.check("guifang_doc",["delete"])
def guifang_docs_id_delete(id,jwt = None):
    return docs_id_delete(Guifang_doc,id)
