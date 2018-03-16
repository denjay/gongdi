########################################
# create by :cxh-pc
# create time :2018-03-15 18:39:24.754692
########################################
from app.models_base import *
from flask import current_app
from sqlalchemy import func
from app import db
from app.utils import get_login_user
import time
import datetime
def new_id():
    sql_url=current_app.config['SQLALCHEMY_DATABASE_URI']
    if sql_url.startswith('mysql+mysqldb'):
        connection = db.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("sp_getobjectids_new", [1])
            newid = cursor.fetchone()[0]
            cursor.close()
            connection.commit()
        finally:
            connection.close()
        # newid = db.session.execute('call sp_getobjectids_new(1,@a);select @a;').fetchone()[0]
    elif sql_url.startswith('mssql+pymssql'):
        newid = db.session.execute(' declare @RETURNVALUE int '
                                   ' exec [dbo].[sp_GetObjectIDs_new] 1, @RETURNVALUE output '
                                   ' select @RETURNVALUE').fetchone()[0]
    return str(newid)
# def new_id():
#     sql_url = current_app.config['SQLALCHEMY_DATABASE_URI']
#     if sql_url.startswith('mysql+mysqldb'):
#         newid = db.session.execute('call sp_getobjectids_new(1); ').fetchone()[0]
#     elif sql_url.startswith('mssql+pymssql'):
#         newid = db.session.execute(' declare @RETURNVALUE int '
#                                    ' exec [dbo].[sp_GetObjectIDs_new] 1, @RETURNVALUE output '
#                                    ' select @RETURNVALUE').fetchone()[0]
#     return str(newid)
def dateformat(str):   #处理时差问题（日期格式传到后台会减8小时变成前一天的问题）
    str=str[:19]
    date = time.strptime(str, '%Y-%m-%dT%H:%M:%S')
    d4 = datetime.datetime(date[0], date[1], date[2])
    date = d4 + datetime.timedelta(days=1)
    return date.strftime('%Y-%m-%d')
class Employee(Employee_base):
    @classmethod
    def check_dateformat(cls, body):
        # 如果包含国际时间或有‘’ 需要处理
        datelist = ['hire_date', 'birth_date', 'join_date', 'cardbeg_date', 'cardend_date', 'leave_date']
        for item in datelist:
            try:
                if not body.get(item):
                    if body.get(item) is not None:
                        body[item] = None
                    continue
                if 'T' in body[item]:
                    body[item] = dateformat(body[item])
            except Exception as err:
                pass
    @classmethod
    def check_valid(cls,data):
        id = data.get('id')
        login_user = data.get('login_user')
        # login_user不能重复
        if login_user:
            # 判断login_user是否被其他员工引用
            count = db.session.query(func.count(Employee.id)).\
                filter(Employee.login_user==login_user,Employee.id!=id).\
                         first()
            if count[0] > 0:
                raise Exception('登录用户(%s)已被使用，请重新指定！' % login_user)
            cuser = get_login_user()
            if cuser.ismanageuser:
                manageid = cuser.uid
            else:
                manageid = cuser.manageuserid
            # 登录用户必须存在，且必须由他的管理者用户新增的
            emp_user = Appuser.query. \
                         filter(Appuser.manageuserid == manageid). \
                         filter(Appuser.name == login_user). \
                         first()
            if not emp_user:
                raise Exception('登录用户(%s)无效，请重新指定！' % login_user)
        return True
    def to_json(self):
        return {"id": self.id,
            "emp_id": self.emp_id,
            "emp_name": self.emp_name,
            "id_card": self.id_card,
            "hire_date": self.hire_date.strftime('%Y-%m-%d') if (not self.hire_date is None) else self.hire_date,
            "address": self.address,
            "sex": self.sex,
            "marriage": self.marriage,
            "birth_date": self.birth_date.strftime('%Y-%m-%d') if (not self.birth_date is None) else self.birth_date,
            "temp_month": self.temp_month,
            "join_date": self.join_date.strftime('%Y-%m-%d') if (not self.join_date is None) else self.join_date,
            "cardbeg_date": self.cardbeg_date.strftime('%Y-%m-%d') if (not self.cardbeg_date is None) else self.cardbeg_date,
            "cardend_date": self.cardend_date.strftime('%Y-%m-%d') if (not self.cardend_date is None) else self.cardend_date,
            "link_man": self.link_man,
            "link_phone": self.link_phone,
            "phone": self.phone,
            "qq": self.qq,
            "email": self.email,
            "leave_date": self.leave_date.strftime('%Y-%m-%d') if (not self.leave_date is None) else self.leave_date,
            "leave_cause": self.leave_cause,
            "login_user": self.login_user,
            "departid": self.departid,
            "departname": self.depart.depart_name,
            "departinsideid": self.depart.inside_id,
            "companyid":self.depart.companyid,
            "code":self.code,
            "nation": self.nation,
            "job_title": self.job_title
            }
class Company(Company_base):
    pass
class Company_auth(Company_auth_base):
    def to_json(self):
        return {"id": self.id,
                "appuserid": self.appuserid,
                "companyid": self.companyid,
                "user_name": '',#self.appuser.name,
                "company_name": self.company.company_name,
                }
class Depart(Depart_base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None
        self.sons = []
    def get_dict(self):
        return {'code': self.code, 'id': self.id, 'companyid': self.companyid, 'inside_id': self.inside_id,
                'depart_name': self.depart_name, 'linkman': self.linkman, 'linktel': self.linktel, 'remark': self.remark}
    def get_sons_dict(self):
        result = []
        for s in self.sons:
            result.append(s.get_dict())
        return result
class Work_experience(Work_experience_base):
    pass
class Emp_degree(Emp_degree_base):
    def to_json(self):
        return {"id": self.id,
              "school_name":self.school_name,
              "department":self.department,
              "study_begin":self.study_begin.strftime('%Y-%m-%d') if (not self.study_begin is None) else self.study_begin,
              "study_end":self.study_end.strftime('%Y-%m-%d') if (not self.study_end is None) else self.study_end,
              "degree_type":self.degree_type,
              "remark":self.remark,
              "degree_name":self.degree_name,
              "employeeid":self.employeeid,
              }
class Appuser(Appuser_base):
    pass
