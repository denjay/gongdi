########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:35.987729
########################################
from app import auth, db, p
from app.models import *
@auth.valid_login
@p.check("illegal_type",["insert"])
def illegal_types_post(body,jwt = None) -> str:
    try:
        data = Illegal_type(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_type",["view"])
def illegal_types_id_get(id,jwt = None) -> str:
    data = Illegal_type.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_type",["edit"])
def illegal_types_id_put(id,body,jwt = None) -> str:
    try:
        Illegal_type.query.filter(Illegal_type.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Illegal_type.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_type",["delete"])
def illegal_types_id_delete(id,jwt = None) -> str:
    try:
        db.session.query(Illegal_type).filter(Illegal_type.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check("illegal_type",["view"])
def illegal_categorys_id_types_get(id,jwt = None) -> str:
    datas = Illegal_type.query.filter(Illegal_type.illegal_categoryid==id).all()
    return [data.to_json() for data in datas],200,{"content-type": "chatset=utf8"}
