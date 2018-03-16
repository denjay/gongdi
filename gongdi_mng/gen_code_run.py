########################################
# create by :cxh-PC
# create time :2018-01-30 21:10:17.863737
########################################
#!/usr/bin/env python

from gencode.gen_code import GenCode,GenProject_Flask

if __name__ == '__main__':
    rootpath = r'.'
    umlfile = r'./docs/gongdi_mng.mdj'
    g = GenCode(umlfile,rootpath)
    #  把boclass 汇出成 swagger class
    g.export(umlfile,umlfile,
             exclude_classes=['illegal','company_auth',
                              'company','employee',
                              'depart','inspect',
                              'doc'])
    #  产生model单元，type= flask:产生flask_sqlalchemy 的 model
    #               type = sql ：产生 sqlalchemy 的 model
    g.model()
    p = GenProject_Flask(umlfile, rootpath)
    # 产生专案代码
    p.gen_code()
