########################################
# create by :cxh-PC
# create time :2018-03-09 11:58:01.782475
########################################
'''
'''
def add_seed(session,cls,flt,datas):
    '''
    增加物件
    :param session: sQLAlchemy session
    :param cls: boclass，如：Employee
    :param flt: 过滤条件，如：{'id':1000,'name':'cxh'}
    :param datas: 物件body，如：
                  {'id':1000,'emp_name':'cxh',
                   'departid':999}
    :return: 企业物件，employee
    '''
    data = session.query(cls).filter_by(**flt).first()
    if not data:
        data = cls(**datas)
        session.add(data)
        session.commit()
    else:
        session.query(cls).filter_by(**flt).update(datas)
    return data
