########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:37.056692
########################################
from app import auth, db, p
from app.models import *
def buwei_id_jishu_docs_get(id,jwt = None) -> str:
    try:
        result = {}
        data = Doc.query.filter(Doc.buweiid==id).all()
        for d in data:
            result.setdefault(d.discriminator,[]).append(d.to_jsonex())
        return result, 200, {"content-type": "chatset=utf8"}
    except Exception as e:
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
