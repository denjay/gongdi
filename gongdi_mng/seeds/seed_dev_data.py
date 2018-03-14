# 开发数据
from app import create_app_swagger,db
from app.models import *
from seeds.seed_utils import add_seed

def init_dev_data():
    app = create_app_swagger('development').app
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    illegal_category1 = add_seed(db.session,Illegal_category,{'name':'质量违规'},{'name':'质量违规'})
    illegal_category2 = add_seed(db.session,Illegal_category,{'name':'安全管理违规'},{'name':'安全管理违规'})
    illegal_type1 = add_seed(db.session,Illegal_type,{'name':'违反操作规程'},
                             {'name':'违反操作规程','illegal_categoryid':illegal_category1.id})
    company1 = add_seed(db.session,Company,{'company_name':'铨鼎科技测试'},{'company_name':'铨鼎科技测试'})
    company_auth = add_seed(db.session,Company_auth,{'appuserid':'1999','companyid':company1.id},{'appuserid':'1999','companyid':company1.id})
    depart1 = add_seed(db.session,Depart,{'companyid':company1.id},{'companyid':company1.id})
    employee = add_seed(db.session,Employee,{'emp_name':'cxh'},{'emp_name':'cxh','departid':depart1.id})
    danti1 = add_seed(db.session,Danti,{'name':'danti1'},{'name':'danti1','description':'danti1desc','companyid':company1.id})
    buwei1 = add_seed(db.session,Buwei,{'name':'buwei1'},{'name':'buwei','description':'buweidesc','dantiid':danti1.id})
    print(Buwei.query.filter(Buwei.id==2).first())
    print(Buwei.query.filter(Buwei.id == 1).first())
    produce_inspect = add_seed(db.session,Produce_inspect,{'insp_emp':'cxh'},{'insp_emp':'cxh','buweiid':danti1.id})
    print(produce_inspect.buwei)
    print(company1.dantis)



