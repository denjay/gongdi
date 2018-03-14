from .test_base import BasicTestCase
from app.models import *
from app import db
class TestEmpIllegal(BasicTestCase):
    def test_data(self):
        ic = Illegal_category()
        ic.name='bbb'
        db.session.add(ic)
        db.session.commit()
        it = Illegal_type()
        it.illegal_categoryid = ic.id
        it.name = 'it1'
        db.session.add(it)
        db.session.commit()
        e1 = Employee()
        db.session.add(e1)
        db.session.commit()
        c1 = Company()
        c1.com_name ='comp 1'
        db.session.add(c1)
        db.session.commit()
        ei = Emp_illegal()
        ei.companyid = c1.id
        ei.illegal_empid = e1.id
        ei.rectify_empid = e1.id
        ei.file_name='xxxxx'
        ei.illegal_typeid=it.id
        db.session.add(ei)
        db.session.commit()
        eis = Emp_illegal.query.all()
        print('emp_illegal:',eis)

        sbc = Subcontractor()
        sbc.comp_name='cccc'
        si = Subcon_illegal()
        si.companyid = c1.id
        # si.illegal_empid = e1.id
        si.rectify_empid = e1.id
        si.file_name='xxxxx'
        si.illegal_typeid=it.id
        si.subcontractorid=sbc.id
        db.session.add(si)
        db.session.commit()
        sis = Subcon_illegal.query.all()
        print('Subcon_illegal:',sis)
        print('illegal:', Illegal.query.all())



