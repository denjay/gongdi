########################################
# create by :sin
# create time :2018-05-04 09:39:27.348626
########################################
from app import auth, db, p
from app.models import Company,Company_auth,Appuser
from app.utils import get_login_user
from flask import g
def get_companys():
    '''
    根据当前用户授权，取出分配给他的权限
    :return:
    '''
    user = get_login_user()
    if user.issystemuser:
        datas = Company.query.all()
    # elif user.ismanageuser:
    #     datas_q1 = Company.query.\
    #         join(User_company_auth,User_company_auth.companyid==Company.id).\
    #         filter(User_company_auth.user_id==user.uid)  #管理者自己创建的公司
    #     datas_q2 = Company.query. \
    #         join(Company_auth, Company_auth.companyid == Company.id). \
    #         filter(Company_auth.appuserid == user.uid)   #其他用户给此管理者授权的公司
    #     datas = datas_q1.union(datas_q2).distinct().all()
    else:
        datas_q1 = Company.query.\
            join(Company_auth,Company_auth.companyid==Company.id).\
            filter(Company_auth.appuserid==user.uid)
        datas = datas_q1.all()
    return datas
@auth.valid_login
def companys_lk_get(jwt = None):
    datas = get_companys()
    return [{"id":data.id,
             "company_name":data.company_name}
            for data in datas], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
# @p.check('company',["view"])
# 公司非敏感资料，可以不鉴权
def companys_get(jwt = None):
    datas = get_companys()
    return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('company',["view"])
def companys_id_get(id,jwt = None):
    data = Company.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('company',["delete"])
def companys_id_delete(id,jwt = None):
    user = get_login_user()
    try:
        if not (user.issystemuser or user.ismanageuser):
            raise Exception('非管理员用户不能删除公司资料!')
        cmp_q = Company.query.filter(Company.id==id)
        if user.ismanageuser:
            cmp_q = cmp_q.filter(Company.create_userid==user.uid)
        cmp = cmp_q.first()
        if cmp is None:
            raise Exception('不能删除非本登入用户创建的公司')
        db.session.delete(cmp)
        # db.session.query(Company).filter(Company.id == id).delete()
        ucas = Company_auth.query.filter(Company_auth.companyid==id).\
            filter(Company_auth.appuserid==g.user_id).all()
        for uca in ucas:
            db.session.delete(uca)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
@auth.valid_login
@p.check('company',["edit"])
def companys_id_put(id,body,jwt = None):
    try:
        if 'companyid' in body and body['companyid']=='':
            body['companyid'] =None
        Company.query.filter(Company.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Company.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check('company',["insert"])
def companys_post(body,jwt = None):
    try:
        user = get_login_user()
        if not (user.issystemuser or user.ismanageuser):
            raise Exception('非管理员用户不能新增公司资料!')
        if body.get('companyid')=='':
            body['companyid'] =None
        body['create_userid'] = user.uid
        data = Company(**body)
        # todo 把管理员的员工做公司授权
        db.session.add(data)
        db.session.commit()
        if user.ismanageuser:
            uca = Company_auth()
            uca.companyid = data.id
            uca.appuserid = user.uid
            db.session.add(uca)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
def companysappid_id_get(id,jwt = None):
    # user = get_login_user()
    # managedatas=db.session.query(Appuser.ismanage).filter_by(id=id).first()
    ismanageuser=False
    # if user.managedatas:
    #     ismanageuser=managedatas.ismanage#判断是不是系统用户
    # if ismanageuser:
    #     datas_q1 = Company.query. \
    #         join(User_company_auth, User_company_auth.companyid == Company.id). \
    #         filter(User_company_auth.user_id == id)  # 管理者自己创建的公司
    #     datas_q2 = Company.query. \
    #         join(Company_auth, Company_auth.companyid == Company.id). \
    #         filter(Company_auth.appuserid == id)  # 其他用户给此管理者授权的公司
    #     datas = datas_q1.union(datas_q2).distinct().all()
    # else:
    datas_q1 = Company.query. \
            join(Company_auth, Company_auth.companyid == Company.id). \
            filter(Company_auth.appuserid == id)
    datas = datas_q1.all()
    return [{"id": data.id,
             "company_name": data.company_name}
            for data in datas], 200, {"content-type": "chatset=utf8"}
