########################################
# create by :sin
# create time :2018-05-04 09:39:27.411823
########################################
from app import auth, db, p
from app.models import *
def health_get(jwt = None):
    result = 'ok'
    return result,200,{'content-type': 'chatset=utf8'}
