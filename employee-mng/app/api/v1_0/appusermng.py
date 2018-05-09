########################################
# create by :sin
# create time :2018-05-04 09:39:27.417838
########################################
from app import auth, db, p
from app.models import *
from sqlalchemy import or_
from app.utils import get_login_user
@auth.valid_login
# @p.check("Appuser",["view"])
def appusers_get(jwt = None):
    try:
        user = get_login_user()
        if user.issystemuser:
            datas = Appuser.query.all()
        elif user.ismanageuser:  #管理者可以看到自己管理的用户
            datas = Appuser.query.filter(or_(Appuser.manageuserid == user.uid,Appuser.id == user.uid)).all()
        else:
            datas = Appuser.query.filter(Appuser.id == user.uid).all()
        return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
