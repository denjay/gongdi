########################################
# create by :cxh-PC
# create time :2018-01-31 11:55:31.654266
########################################
#!/usr/bin/env bash
# consul的host 格式 ip:port
export CONSUL_HTTP_ADDR=192.168.101.88:8500
# docker host的port
export WEB_PORT=8899
# true自動註冊到kong，true，false不做，注意字母全小寫
export KONG_AUTO_REGISTER=true
# true自動註冊成 consul服務，false不做，注意字母全小寫
export CONSUL_AUTO_REGISTER=true
# 资料库名，默认为 maxbus
export DATABASE_NAME=scsdb
# 权限用的系统名称
export SYSTEM_NAME=scs
export LOG_LEVEL=20
# 保存文档的根目录
export UPLOAD_FOLDER="/var/gongdi_mng/store"
# 開發環境的docker，代碼valume方式
docker-compose -f docker-compose-dev.yaml up -d
# 部署的docker-compose 文件
#docker-compose up -d
