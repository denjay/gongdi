########################################
# create by :cxh-PC
# create time :2017-09-09 17:49:43.687273
########################################

### install package
```
pip install -r requirements.txt

```
### run
python run.py

### swagger debug:


```
http://localhost:8011/employeemng/v1.0/ui/

```

### redis install(redis 3.2)
1. uninstall redis : pip uninstall redis
2. install : pip install git+https://github.com/andymccurdy/redis-py.git



### 环境变量设定
```
True：自動註冊到kong
auto_register2kong = os.environ.get('kong_auto_register') or  conf_parse.getboolean('reg_service','kong',fallback=False)
True:自動註冊到consul
auto_register2consul = os.environ.get('consul_auto_register') or  conf_parse.getboolean('reg_service','consul',fallback=False)
web_port =os.environ.get('web_port') or conf_parse.getint('web','port',fallback=8000)
```

### 执行docker
  sudo ./run.sh



