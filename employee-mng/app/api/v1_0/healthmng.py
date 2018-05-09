########################################
# create by :cxh-pc
# create time :2018-03-15 18:39:26.907715
########################################
from app import auth, db, p
from app.models import *
def health_get(jwt = None):
    result = 'ok'
    return result,200,{'content-type': 'chatset=utf8'}
