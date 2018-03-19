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

    # 智慧工地系统
    scs = add_sys1('mis0','scs')
    # 违规管理
    illegalmng = add_sys2(scs,'illegalmng','违规管理')
    #   违规种类
    illegal_category = add_sys3_and_op(scs,illegalmng,'Illegal_category','违规种类')
    #   违规类型
    illegal_type = add_sys3_and_op(scs,illegalmng,'Illegal_type','违规类型')
    #   分包商
    subcontractor = add_sys3_and_op(scs,illegalmng,'Subcontractor','分包商')
    #   员工违规
    emp_illegal=add_sys3_and_op(scs,illegalmng,'Emp_illegal','员工违规')
    #   分包商违规
    subcon_illegal=add_sys3_and_op(scs,illegalmng,'Subcon_illegal','分包商违规')
    #   违规图片
    illegal_pic = add_sys3(scs,illegalmng,'illegal_pic','违规图片')
    add_sys3_op(illegal_pic, 'view', '浏览图片', 1)
    add_sys3_op(illegal_pic, 'insert', '上传图片',2)
    add_sys3_op(illegal_pic, 'delete', '删除图片', 4)
    # 质量管理
    zhiliangmng = add_sys2(scs, 'zhiliangmng', '质量管理')
    #   质量巡检
    quality_inspect=add_sys3_and_op(scs,zhiliangmng,'Quality_inspect','质量巡检')
    # 安全管理
    safetymng = add_sys2(scs, 'safetymng', '安全管理')
    #   安全巡检
    safety_inspect = add_sys3_and_op(scs,safetymng,'Safety_inspect','安全巡检')
    # 生产管理
    producemng = add_sys2(scs, 'producemng', '生产管理')
    #   生产巡检
    produce_inspect=add_sys3_and_op(scs,producemng,'Produce_inspect','生产巡检')
    # 巡检图片管理
    inspect_picmng = add_sys2(scs, 'inspect_picmng', '巡检图片管理')
    #   巡检图片
    inspect_pic = add_sys3(scs,inspect_picmng,'inspect_pic','巡检图片')
    add_sys3_op(inspect_pic, 'view', '浏览图片', 1)
    add_sys3_op(inspect_pic, 'insert', '上传图片',2)
    add_sys3_op(inspect_pic, 'delete', '删除图片', 4)
    # 技术管理
    jishumng = add_sys2(scs, 'jishumng','技术管理')
    #   工地管理
    gongdi = add_sys3_and_op(scs,jishumng,'gongdi','工地管理')
    #   单体管理
    danti = add_sys3_and_op(scs,jishumng,'danti','单体管理')
    #   部位管理
    buwei = add_sys3_and_op(scs,jishumng,'buwei','部位管理')
    #   规范管理
    guifang_doc = add_sys3_and_op(scs,jishumng,'guifang_doc','规范管理')
    #   图纸管理
    tuzhi_doc = add_sys3_and_op(scs,jishumng,'tuzhi_doc','图纸管理')
    #   图集管理
    tuji_doc=add_sys3_and_op(scs,jishumng,'tuji_doc','图集管理')
    #   交底管理
    jiaodi_doc = add_sys3_and_op(scs,jishumng,'jiaodi_doc','交底管理')
    #   巡检图片
    doc_file = add_sys3(scs,jishumng,'doc_file','文档附件')
    add_sys3_op(doc_file, 'view', '浏览/下载', 1)
    add_sys3_op(doc_file, 'insert', '上传附件',2)
    add_sys3_op(doc_file, 'delete', '删除附件', 4)
    current_app.logger.info('add right seeds success!')

