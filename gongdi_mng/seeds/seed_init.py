'''
系统默认资料的初始化
'''
from app import create_app_swagger
from app.models import *
from seeds.seed_utils import add_seed

def init_default_data(config):
    app = create_app_swagger(config).app
    app_context = app.app_context()
    app_context.push()
    app.logger.info('start add default seeds ')
    db.create_all()
    illegal_category1 = add_seed(db.session,Illegal_category,{'name':'质量违规'},{'name':'质量违规'})
    add_seed(db.session,Illegal_type,{'name':'擅自降低工程质量标准，采用以次充好'},
                             {'name':'擅自降低工程质量标准，采用以次充好','illegal_categoryid':illegal_category1.id})
    add_seed(db.session,Illegal_type,{'name':'擅自减少操作环节，偷工减料'},
                             {'name':'擅自减少操作环节，偷工减料','illegal_categoryid':illegal_category1.id})
    add_seed(db.session,Illegal_type,{'name':'上道工序未经验收，擅自进行下道工序'},
                             {'name':'上道工序未经验收，擅自进行下道工序','illegal_categoryid':illegal_category1.id})
    add_seed(db.session,Illegal_type,{'name':'工程定位防线未经检查验收擅自使用记录'},
                             {'name':'工程定位防线未经检查验收擅自使用记录','illegal_categoryid':illegal_category1.id})
    add_seed(db.session,Illegal_type,{'name':'擅自改变配比，降低标高'},
                             {'name':'擅自改变配比，降低标高','illegal_categoryid':illegal_category1.id})
    add_seed(db.session,Illegal_type,{'name':'建筑材料进场未经验收、检测擅自使用'},
                             {'name':'建筑材料进场未经验收、检测擅自使用','illegal_categoryid':illegal_category1.id})
    add_seed(db.session,Illegal_type,{'name':'隐蔽工程未经验收擅自进行隐蔽'},
                             {'name':'隐蔽工程未经验收擅自进行隐蔽','illegal_categoryid':illegal_category1.id})
    add_seed(db.session,Illegal_type,{'name':'采取不合理的工期，随意压缩工期的'},
                             {'name':'采取不合理的工期，随意压缩工期的','illegal_categoryid':illegal_category1.id})
    illegal_category2 = add_seed(db.session,Illegal_category,{'name':'安全管理违规'},{'name':'安全管理违规'})
    add_seed(db.session,Illegal_type,{'name':'违规操作施工机械'},
                             {'name':'违规操作施工机械','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'不持证上岗'},
                             {'name':'不持证上岗','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'违反操作规程'},
                             {'name':'违反操作规程','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'不按照施工方案及施工组织设计进行施工'},
                             {'name':'不按照施工方案及施工组织设计进行施工','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'施工机械不按期保养、检查、检测'},
                             {'name':'施工机械不按期保养、检查、检测','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'不按规定进行基坑防护'},
                             {'name':'不按规定进行基坑防护','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'擅自拆除塔吊、施工电梯、吊栏等施工机械的限位装置'},
                             {'name':'擅自拆除塔吊、施工电梯、吊栏等施工机械的限位装置','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'现场用电私拉乱扯'},
                             {'name':'现场用电私拉乱扯','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'不按规定，配备防护装置'},
                             {'name':'不按规定，配备防护装置','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'私自拆除脚手架的连墙杆件'},
                             {'name':'私自拆除脚手架的连墙杆件','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'施工作业面防护高度不足'},
                             {'name':'施工作业面防护高度不足','illegal_categoryid':illegal_category2.id})
    add_seed(db.session,Illegal_type,{'name':'对临边、洞口、楼梯、电梯井等部位不进行防护'},
                             {'name':'对临边、洞口、楼梯、电梯井等部位不进行防护','illegal_categoryid':illegal_category2.id})

    app.logger.info('add default seeds success')