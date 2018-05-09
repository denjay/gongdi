########################################
# create by :cxh-PC
# create time :2017-12-13 19:30:42.116728
########################################
import connexion
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from mwauth.kong_auth import KongAuth
from mwauth.redis_session import RedisSessionInterface
from config import config
from flask_cors import CORS
from mwpermission.permission import Permission
import logging

db = SQLAlchemy()
rds = FlaskRedis(strict=False)
auth = KongAuth()
p = Permission()

def create_app_swagger(config_name):
    conf = config[config_name]
    app_swg = connexion.App(__name__,
                            port = conf.PORT,
                            debug= conf.DEBUG,
                            specification_dir='../swagger/'
                            )
    yaml_host=app_swg.add_api('./v1_0/employeemng.yaml', arguments={'title': 'api v1.0'})
    app = app_swg.app
    app.session_interface = RedisSessionInterface(app, rds)
    CORS(app)
    app.config.from_object(conf)
    config[config_name].init_app(app)
    # from app.model import AuthUser
    # auth.user_class = AuthUser
    # 如果服務不需要註冊到kong，需修改host的設定
    if app.config['KONG_AUTO_REGISTER']:
        from mwsdk import Kong
        kong = Kong()
        yaml_host.specification['host'] = '%s:%s'%(kong.ip,kong.port)
    else:
        from mwsdk import consul_agent_conf
        yaml_host.specification['host'] = '%s:%s' % (consul_agent_conf.bind_ip, app.config['PORT'])
    # 需要增加handler 这样docker 中才能看到log
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    app.logger.addHandler(consoleHandler)
    app.logger.level = app.config['LOG_LEVEL']
    db.init_app(app)
    rds.init_app(app)
    auth.init_app(app)
    p.init_app(app)
    return app_swg

