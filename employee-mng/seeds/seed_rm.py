########################################
# create by :cxh-PC
# create time :2018-03-09 11:58:01.772415
########################################
'''
初始化权限资料
'''
from seeds.models_rm import *
from app.models import *
from app import create_app_swagger
def init_rm_data(config):
    app = create_app_swagger(config).app
    app_context = app.app_context()
    app_context.push()
    current_app.logger.info('start add right seeds ')
    db.create_all()
    # 第一层权限
    sys1 = add_sys1('mis0', 'scs')
    # 第二层权限
    sys2 = add_sys2(sys1,'hrmng','人事管理')
    # 第三层权限和操作
    add_sys3_and_op(sys1, sys2, 'company','公司管理')
    add_sys3_and_op(sys1, sys2, 'depart','部门管理')
    add_sys3_and_op(sys1, sys2, 'employee','员工管理')
    add_sys3_and_op(sys1, sys2, 'emp_degree','教育经历')
    add_sys3_and_op(sys1, sys2, 'work_experience','工作经历')
    add_sys3_and_op(sys1, sys2, 'companyauth','公司授权')
    current_app.logger.info('add right seeds success!')
