########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:35.906655
########################################
from app import auth, db, p
from app.models import *
@auth.valid_login
@p.check("illegal_category",["view"])
def illegal_categorys_get(jwt = None) -> str:
    data = Illegal_category.query.all()
    return [data.to_json() for data in data], \
           200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_category",["insert"])
def illegal_categorys_post(body,jwt = None) -> str:
    try:
        data = Illegal_category(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_category",["view"])
def illegal_categorys_id_get(id,jwt = None) -> str:
    data = Illegal_category.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_category",["edit"])
def illegal_categorys_id_put(id,body,jwt = None) -> str:
    try:
        Illegal_category.query.filter(Illegal_category.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Illegal_category.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("illegal_category",["delete"])
def illegal_categorys_id_delete(id,jwt = None) -> str:
    try:
        db.session.query(Illegal_category).filter(Illegal_category.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
