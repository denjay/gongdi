########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.254755
########################################
from app import auth, db, p
from app.models import *
def health_() -> str:
    pass
def health_get():
    try:
        data = {}
        return data, 200, {"content-type": "chatset=utf8"}
    except Exception as e:
        # todo handle error
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
