########################################
# create by :sin
# create time :2017-06-28 11:29:09.532101
########################################
#!/usr/bin/env python
from gencode.gen_code import GenCode,GenProject_Flask
if __name__ == '__main__':
    rootpath = r'.'
    xmifile = r'./docs/employee-bo.mdj'
    g = GenCode(xmifile,rootpath)
    g.model()
    p = GenProject_Flask(xmifile, rootpath)
    p.gen_code()