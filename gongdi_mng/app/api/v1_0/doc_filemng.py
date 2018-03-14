########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:36.819479
########################################
from app import auth,p,db
from app.models import *
import os
from flask import current_app,send_file
from app.utils import get_file_name
import unicodedata
import urllib
@auth.valid_login
@p.check("doc_file",["view"])
def docs_docsid_files_get(docsid,jwt = None) -> str:
    datas = Doc_file.query.filter(Doc_file.docid==docsid).all()
    return [data.to_json() for data in datas],200,{"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("doc_file",["view"])
def doc_files_id_get(id,jwt = None) -> str:
    data = Doc_file.query.filter_by(id=id).first_or_404()
    # filename_s, ext_name = data.file_name.rsplit('.', 1)
    rv = send_file(filename_or_fp=data.save_file_name,
                   as_attachment=True)
    # 中文名称用utf-8
    filenames = {'filename': unicodedata.normalize('NFKD', data.file_name).encode('latin-1', 'ignore'),
                 'filename*': "UTF-8''{}".format(urllib.parse.quote(data.file_name))}
    rv.headers.set('Content-Disposition', 'attachment', **filenames)
    return rv
@auth.valid_login
@p.check("doc_file",["delete"])
def doc_files_id_delete(id,jwt = None) -> str:
    try:
        doc_file = Doc_file.query.filter(Doc_file.id == id).first()
        if doc_file:
            try:
                os.remove(doc_file.save_file_name)
            except Exception as e:
                pass
            db.session.delete(doc_file)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check("doc_file",["insert"])
def doc_files_post(doc,docsid,jwt = None) -> str:
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],'docs')
        os.makedirs(file_path,exist_ok=True)
        # 真实存储的文件增加秒数，防止被覆盖
        file_name = get_file_name(doc.filename,file_path)
        doc.save(file_name)
        data = Doc_file(file_name=doc.filename,
                         file_size=round(os.path.getsize(file_name)/1024,2),
                         save_file_name=file_name,
                         docid=docsid)
        db.session.add(data)
        db.session.commit()
        return data.to_json(), \
               201, {"content-type": "chatset=utf8"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
