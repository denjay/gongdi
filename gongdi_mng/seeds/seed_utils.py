

def add_seed(session,cls,flt,datas):
    data = session.query(cls).filter_by(**flt).first()
    if not data:
        data = cls(**datas)
        session.add(data)
        session.commit()
    else:
        session.query(cls).filter_by(**flt).update(datas)
    return data