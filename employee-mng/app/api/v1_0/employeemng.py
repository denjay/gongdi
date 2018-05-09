########################################
# create by :cxh-pc
# create time :2018-03-15 18:39:26.853676
########################################
from app import auth,db,p
from sqlalchemy import or_
from app.models import Employee,Depart,Company,Company_auth,new_id
import time,datetime
from app.utils import get_login_user
#import csv
@auth.valid_login
@p.check('employee',["view"])
def employees_id_get(id,jwt = None):
    data = Employee.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('employee',["delete"])
def employees_id_delete(id,jwt = None):
    try:
        db.session.query(Employee).filter(Employee.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check('employee',["edit"])
def employees_id_put(id,body,jwt = None):
    try:
        if not Employee.check_valid({'id':id,'login_user':body.get('login_user')}):
            raise Exception('登录用户(%s)已被使用，请重新指定！'% body.get('login_user'))
        if type(id)!='int':
            id=int(id)
        Employee.check_dateformat(body)
        Employee.query.filter(Employee.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error":str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Employee.query.filter_by(id=id).first_or_404()
    # data.cids = ','
    # for auth in data.company_auths:
    #     data.cids += str(auth.companyid) + ','
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('employee',["insert"])
def employees_post(body,jwt = None):
    try:
        if not Employee.check_valid({'id':None,'login_user':body.get('login_user')}):
            raise Exception('登录用户(%s)已被使用，请重新指定！'% body.get('login_user'))
        Employee.check_dateformat(body)
        if 'cids' in body:
            body.pop('cids')
        if 'departname' in body:
            body.pop('departname')
        if 'companyid' in body:
            body.pop('companyid')
        if 'departinsideid' in body:
            body.pop('departinsideid')
        data = Employee(**body)
        db.session.add(data)
        db.session.commit()
        # data.cids = ','
        # for auth in data.company_auths:
        #     data.cids += str(auth.companyid) + ','
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
def dateformat(str):   #处理时差问题（日期格式传到后台会减8小时变成前一天的问题）
    str=str[:19]
    date = time.strptime(str, '%Y-%m-%dT%H:%M:%S')
    d4 = datetime.datetime(date[0], date[1], date[2])
    date = d4 + datetime.timedelta(days=1)
    return date.strftime('%Y-%m-%d')
def get_employees(emp_name = None,page = None,perpage = None):
    user = get_login_user()
    if user.issystemuser:
        datap = Employee.query
    else:
        # Employee_login = aliased(Employee)
        # 授权公司的员工
        datap = Employee.query.\
            join(Depart, Depart.id == Employee.departid).\
            join(Company, Company.id == Depart.companyid).\
            join(Company_auth, Company_auth.companyid == Company.id).\
          filter(Company_auth.appuserid == user.uid)
    if emp_name is not None:
        datap = datap.filter(Employee.emp_name.like('%'+'%s'%emp_name+'%'))
    datap = datap.order_by(Employee.emp_name).distinct().paginate(page,perpage)
    return datap.total,datap.items
@auth.valid_login
@p.check('employee',["view"])
def employees_get(page = None,perpage = None,emp_name = None,jwt = None):
    try:
        total,datas = get_employees(emp_name,page,perpage)
        return [data.to_json() for data in datas], 200, \
               {"content-type": "chatset=utf8","X-Page":page,"X-Total":total}
    except Exception as e:
        return {"error": str(e), "success": False}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
def employees_lk_get(page = None,perpage = None,emp_name = None,jwt = None):
    to_json = lambda item: {"id": item.id,
                            "emp_name": item.emp_name,
                            "emp_id": item.emp_id,
                            "id_card": "string"}
    try:
        total,datas = get_employees(emp_name,page,perpage)
        return [to_json(data) for data in datas], 200, \
               {"content-type": "chatset=utf8","X-Page":page,"X-Total":total}
    except Exception as e:
        return {"error": str(e), "success": False}, 422, {"content-type": "chatset=utf8"}
def get_depart_id_empolyees(id,page = None,perpage = None,emp_name = None):
    if int(id) < 0:
        id = -int(id)
        if (page == None and perpage == None):
            if emp_name:
                data = db.session.query(Employee).\
                          join(Depart, Depart.id == Employee.departid).\
                          join(Company,Company.id == Depart.companyid).\
                         filter(Company.id == id). \
                         filter(Employee.emp_name.like('%' + emp_name + '%'))
            else:
                data = db.session.query(Employee).\
                    join(Depart, Depart.id == Employee.departid).\
                    join(Company,Company.id == id).all()
            total = len(data)
            datas = data
        else:
            data = Employee.query.\
                   join(Depart, Depart.id == Employee.departid).\
                   join(Company,Company.id == Depart.companyid).\
                   filter(Company.id == id)
            if emp_name and emp_name != '':
                data = data.filter(Employee.emp_name.like('%' + emp_name + '%'))
            data = data.order_by(Employee.id).paginate(page, perpage, False)
            datas = data.items
            total = data.total
    else:
        if (page == None and perpage == None):
            data = data = Employee.query.join(Depart, Depart.id == Employee.departid).filter(
                or_(Depart.id == id, Depart.inside_id.like('%-' + str(id) + '-%'))).all()
            total = len(data)
            datas = data
        else:
            data = Employee.query.join(Depart, Depart.id == Employee.departid).filter(
                or_(Depart.id == id, Depart.inside_id.like('%-' + str(id) + '-%')))
            if emp_name and emp_name != '':
                data = data.filter(Employee.emp_name.like('%' + emp_name + '%'))
            data = data.order_by(Employee.id).paginate(page, perpage, False)
            datas = data.items
            total = data.total
    return total,datas
@auth.valid_login
def depart_id_employees_lk_get(id,page = None,perpage = None,emp_name = None,jwt = None):
    def to_lk_json(item):
        return {'id':item.id,
                'emp_name':item.emp_name,
                'emp_id':item.emp_id,
                'id_card':item.id_card}
    try:
        total,datas = get_depart_id_empolyees(id,page,perpage,emp_name)
        return {"success": True, "total": total, "data": [to_lk_json(item) for item in datas]}, 200, {
            "content-type": "chatset=utf8"}
    except Exception as e:
        return {"error": str(e), "success": False}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('employee',["view"])
def depart_id_employees_get(id,page = None,perpage = None,emp_name = None,jwt = None):
    try:
        total,datas = get_depart_id_empolyees(id,page,perpage,emp_name)
        return {"success": True, "total": total, "data": [item.to_json() for item in datas]}, 200, {
            "content-type": "chatset=utf8"}
    except Exception as e:
        return {"error": str(e), "success": False}, 422, {"content-type": "chatset=utf8"}
@auth.valid_login
def import_csv_post(file_csv,jwt = None):
    return ''
import sys,os
import xlrd
import tempfile
from werkzeug.utils import secure_filename
import time
ALLOWED_EXTENSIONS = set(['xls'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@auth.valid_login
def import_xls_post(file_csv,jwt = None):
    def analyze_xls():
        s = file_csv.stream.read()
        data = xlrd.open_workbook(file_contents=s)
        table = data.sheets()[0]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        if ncols != 13:
            raise Exception('资料格式错误，请检查')
        datas = {}
        for i in range(1, nrows):
            ems = table.row_values(i)  # 某一行数据
            scname = ems[7].strip()
            if scname == '':
                scname = '空'
            dename = ems[8].strip()
            if dename == '':
                dename = '空'
            if scname in datas:
                deobj = datas[scname]
                if dename in deobj:
                    deobj[dename] += [ems]
                else:
                    deobj[dename] = [ems]
            else:
                datas[scname] = {dename: [ems]}
        return datas
    try:
        errmsg=''
        d=str(int(time.time()))
        empid=0
        if file_csv and allowed_file(file_csv.filename):
            datas=analyze_xls()
            cdatas=dict(db.session.query(Company.company_name,Company.id).all())
            user = get_login_user()
            if not (user.issystemuser or user.ismanageuser):
                raise Exception('非管理员用户不能新增公司资料!')
            ee_indexs=[]#避免员工重复，跨公司跨部门
            for ckey in datas:
                #判断公司是否已经存在
                try:
                    if ckey in cdatas:
                        scid = cdatas[ckey]
                    else:
                        data = Company(company_name=ckey,company_code=ckey,create_userid=user.uid)
                        db.session.add(data)
                        db.session.commit()
                        scid = data.id
                        if user.ismanageuser:
                            uca = Company_auth()
                            uca.id=new_id()
                            uca.companyid = data.id
                            uca.appuserid = user.uid
                            db.session.add(uca)
                            db.session.commit()
                    dess=datas[ckey]
                    ddatas = dict(db.session.query(Depart.depart_name, Depart.id).filter(Depart.companyid== scid).all())
                    for dkey in dess:
                        if dkey in ddatas:
                            did=ddatas[dkey]
                        else:
                            data = Depart(depart_name=dkey,companyid=scid,code=dkey,inside_id='')
                            db.session.add(data)
                            db.session.commit()
                            did=data.id
                        ess=dess[dkey]
                        edatas = dict(db.session.query(Employee.code, Employee.id).filter(Employee.departid == did).all())
                        for item in ess:
                            if item[0] in ee_indexs:
                                continue
                            if item[6]=='未婚':
                                marriage='0'
                            elif item[6]=='已婚':
                                marriage = '1'
                            elif item[6]=='离婚':
                                marriage = '2'
                            elif item[6]=='丧偶':
                                marriage = '3'
                            elif item[6]=='其他':
                                marriage='4'
                            else:
                                marriage = '5'
                            id_card=item[4]
                            if len(id_card)==18:
                                bdate=datetime.datetime.strptime(id_card[6:14], "%Y%m%d")
                            else:
                                bdate=None
                            if item[12]!='':
                                hire_date=datetime.datetime.strptime(item[12], "%Y-%m-%d")
                            else:
                                hire_date =None
                            body={
                                #'emp_id':item[0],
                                'emp_name':item[1],
                                'sex':1 if item[2]=='女' else 0,
                                'id_card':item[4],
                                'marriage':marriage,
                                'departid':did,
                                'code':item[0],
                                'nation':item[5],
                                'job_title':item[10],
                                'hire_date':hire_date,
                                'birth_date':bdate
                            }
                            try:
                                if item[1].strip()=='':
                                    raise Exception('工号['+item[0]+']姓名为空\n')
                                if item[0].strip()=='':
                                    raise Exception('姓名['+item[1]+']工号为空\n')
                                if item[4].strip()=='':
                                    raise Exception('姓名['+item[1]+']身份证号码为空\n')
                                if item[0] in edatas:
                                    Employee.query.filter(Employee.code == item[0]).filter(Employee.departid == did).update(body)
                                else:
                                    empid += 1
                                    data = Employee(**body)
                                    data.emp_id=d+str(empid)
                                    db.session.add(data)
                                    db.session.commit()
                                ee_indexs += [item[0]]
                            except Exception as ee:
                                db.session.rollback()
                                errmsg+= str(ee)
                except Exception as sce:
                    db.session.rollback()
                    errmsg += str(sce)
        if errmsg!='':
            return '有未被导入的数据，信息如下:\n'+errmsg, 422, {"content-type": "chatset=utf8"}
        else:
            return file_csv.filename, 201, {"content-type": "chatset=utf8"}
    except Exception as e:
        # todo handle error
        db.session.rollback()
        return str(e), 422, {"content-type": "chatset=utf8"}
