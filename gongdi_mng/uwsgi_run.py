########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.317254
########################################
from app import create_app_swagger

def register_service(config_name,app):
    from config import config
    # 注册本服务到kong
    config =  config[config_name]
    auto_register2consul = config.CONSUL_AUTO_REGISTER
    auto_register2kong = config.KONG_AUTO_REGISTER
    web_port = config.PORT
    from mwsdk import AgentConf
    service_host = '%s:%s'%(AgentConf().bind_ip,web_port)
    app.logger.info('auto_register2kong:%s'%auto_register2kong)
    if auto_register2kong:
        from mwsdk import Kong
        kong = Kong()
        kong.reg_service('gongdi_mng/v1.0', service_host, auth='jwt')
        app.logger.info('注册kong成功')
        #kong.reg_service('xxxx/v1.0/login_jwt', service_host, auth='')
        #kong.reg_service('xxxx/v1.0/logout_jwt', service_host,auth='jwt')
        #kong.reg_service('static', service_host, auth='', kong_uris='/auth/static')
    # 註冊到kong的服務到consul
    app.logger.info('auto_register2consul:%s'%auto_register2consul)
    if auto_register2consul:
        check = {"id": "gongdi_mng api",
                 "name": "gongdi_mng on port %s"%web_port,
                 "http": "http://%s/gongdi_mng/v1.0/health"%service_host,
                 "interval": "20s",
                 "timeout": "10s",
                 "DeregisterCriticalServiceAfter": "5m"
                 }
        from mwsdk import Kong, reg_service
        kong = Kong()
        reg_service('gongdi_mng',address=kong.ip, port=kong.port, tags=['kong','jwt'],
                    check=check)
        app.logger.info('注册consul成功')

app = create_app_swagger('default')
register_service('default',app.app)
application = app.app


