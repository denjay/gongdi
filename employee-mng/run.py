########################################
# create by :cxh-PC
# create time :2017-12-13 19:30:42.134350
########################################
from app import create_app_swagger

def register_service(config_name,app):
    from config import config
    # 注册本服务到kong
    config =  config[config_name]
    auto_register2consul = config.CONSUL_AUTO_REGISTER
    auto_register2kong = config.KONG_AUTO_REGISTER
    web_port = config.PORT
    from mwsdk import consul_agent_conf
    service_host = '%s:%s'%(consul_agent_conf.bind_ip,web_port)
    if auto_register2kong:
        from mwsdk import Kong
        kong = Kong()
        kong.reg_service('employeemng/v1.0', service_host, auth='jwt')
        app.logger.info('注册kong成功')
        #kong.reg_service('xxxx/v1.0/login_jwt', service_host, auth='')
        #kong.reg_service('xxxx/v1.0/logout_jwt', service_host,auth='jwt')
        #kong.reg_service('static', service_host, auth='', kong_uris='/auth/static')
    # 註冊到kong的服務到consul
    if auto_register2consul:
        check = {"id": "employeemng api",
                 "name": "employeemng on port %s"%web_port,
                 "http": "http://%s/employeemng/v1.0/health"%service_host,
                 "interval": "20s",
                 "timeout": "10s",
                 "DeregisterCriticalServiceAfter": "5m"
                 }
        from mwsdk import Kong, reg_service
        kong = Kong()
        reg_service('employeemng',address=kong.ip, port=kong.port, tags=['kong','jwt'],
                    check=check)
        app.logger.info('注册consul成功')

if __name__ == '__main__':
    app = create_app_swagger('default')
    register_service('default',app.app)
    app.run(host='0.0.0.0')
    if app.config.get('CONSUL_AUTO_REGISTER'):
        from mwsdk import Kong, dereg_service
        dereg_service('employeemng', Kong().port)



