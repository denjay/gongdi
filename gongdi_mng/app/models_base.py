########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:23.146142
########################################
from app import db
from datetime import datetime,timedelta
import json
from enum import Enum
class Auditing_status(Enum):
    unaudited =1
    audit_failed =3
    audit_passed =2
class Illegal(db.Model):
    __tablename__ = 'illegal'
    discriminator = db.Column("type",db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}
    illegal_time = db.Column(db.DateTime)
    rectify_time = db.Column(db.DateTime)
    memo = db.Column(db.String(200))
    recorder = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)
    auditing_status = db.Column(db.Integer)
    rectify_empid = db.Column(db.Integer,db.ForeignKey("employee.id"))
    illegal_typeid = db.Column(db.Integer,db.ForeignKey("illegal_type.id"), nullable= False)
    companyid = db.Column(db.Integer,db.ForeignKey("company.id"), nullable= False)
    rectify_emp = db.relationship("Employee", foreign_keys="Illegal.rectify_empid")
    illegal_type = db.relationship("Illegal_type", foreign_keys="Illegal.illegal_typeid")
    company = db.relationship("Company", foreign_keys="Illegal.companyid")
    illegal_pics = db.relationship("Illegal_pic", back_populates="illegal", foreign_keys="Illegal_pic.illegalid", cascade="all, delete-orphan")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Inspect(db.Model):
    __tablename__ = 'inspect'
    discriminator = db.Column("type",db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}
    id = db.Column(db.Integer, primary_key=True)
    is_qualified = db.Column(db.Boolean, default= False)
    insp_date = db.Column(db.Date)
    insp_emp = db.Column(db.String(50))
    description = db.Column(db.String(50))
    buweiid = db.Column(db.Integer,db.ForeignKey("buwei.id"), nullable= False)
    buwei = db.relationship("Buwei", foreign_keys="Inspect.buweiid")
    inspect_pics = db.relationship("Inspect_pic", back_populates="inspect", foreign_keys="Inspect_pic.inspectid", cascade="all, delete-orphan")
    def to_jsonex(self):
        data = self.to_json()
        data['buwei_name'] = self.buwei.name
        return data
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Buwei(db.Model):
    __tablename__ = 'buwei'
    discriminator = db.Column("type",db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}
    name = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    dantiid = db.Column(db.Integer,db.ForeignKey("buwei.id"))
    danti = db.relationship("Danti", back_populates="buweis", foreign_keys="Buwei.dantiid", remote_side=[id])
    def to_jsonex(self):
        data = self.to_json()
        data['danti_name']=self.danti.name if self.danti else '' 
        return data
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Doc(db.Model):
    __tablename__ = 'doc'
    discriminator = db.Column("type",db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(50))
    description = db.Column(db.String(250))
    buweiid = db.Column(db.Integer,db.ForeignKey("buwei.id"), nullable= False)
    buwei = db.relationship("Buwei", foreign_keys="Doc.buweiid")
    doc_files = db.relationship("Doc_file", back_populates="doc", foreign_keys="Doc_file.docid", cascade="all, delete-orphan")
    def to_jsonex(self):
        data = self.to_json()
        data['buwei_name']=self.buwei.name if self.buwei else ''
        return data
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Emp_illegal(Illegal):
    __mapper_args__ = {'polymorphic_identity': 'emp_illegal'}
    illegal_empid = db.Column(db.Integer,db.ForeignKey("employee.id"))
    illegal_emp = db.relationship("Employee", foreign_keys="Emp_illegal.illegal_empid")
    def to_jsonex(self):
        # 修改代码后需同步到类图，否则重新产生代码会被覆盖
        data = self.to_json()
        data['rectify_emp_name'] = self.rectify_emp.emp_name if self.rectify_emp else ''
        data['illegal_emp_name'] = self.illegal_emp.emp_name if self.illegal_emp else ''
        data['illegal_type_name'] = self.illegal_type.name if self.illegal_type else ''
        data['comp_name'] = self.company.company_name if self.company else ''
        return data
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Subcon_illegal(Illegal):
    __mapper_args__ = {'polymorphic_identity': 'subcon_illegal'}
    subcontractorid = db.Column(db.Integer,db.ForeignKey("subcontractor.id"))
    subcontractor = db.relationship("Subcontractor", foreign_keys="Subcon_illegal.subcontractorid")
    def to_jsonex(self):
        # 需在类图中增加，否则重新产生代码会被覆盖
        data = self.to_json()
        data['illegal_type_name'] = self.illegal_type.name if self.illegal_type else ''
        data['subcon_com_name'] = self.subcontractor.comp_name if self.subcontractor else ''
        data['rectify_emp_name'] = self.rectify_emp.emp_name if self.rectify_emp else ''
        return data
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Illegal_category_base(db.Model):
    __tablename__ = 'illegal_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique= True, nullable= False)
    illegal_types = db.relationship("Illegal_type", back_populates="illegal_category", foreign_keys="Illegal_type.illegal_categoryid", cascade="all, delete-orphan")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Illegal_type_base(db.Model):
    __tablename__ = 'illegal_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique= True, nullable= False)
    illegal_categoryid = db.Column(db.Integer,db.ForeignKey("illegal_category.id"), nullable= False)
    illegal_category = db.relationship("Illegal_category", back_populates="illegal_types", foreign_keys="Illegal_type.illegal_categoryid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Subcontractor_base(db.Model):
    __tablename__ = 'subcontractor'
    id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.String(50))
    tel = db.Column(db.String(50))
    manager = db.Column(db.String(50))
    license = db.Column(db.String(50))
    email = db.Column(db.String(50))
    approach_date = db.Column(db.Date)
    departure_date = db.Column(db.Date)
    companyid = db.Column(db.Integer,db.ForeignKey("company.id"), nullable= False)
    company = db.relationship("Company", foreign_keys="Subcontractor.companyid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Illegal_pic_base(db.Model):
    __tablename__ = 'illegal_pic'
    file_name = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)
    pic_size = db.Column(db.Float)
    save_file_name = db.Column(db.String(250))
    illegalid = db.Column(db.Integer,db.ForeignKey("illegal.id"), nullable= False)
    illegal = db.relationship("Illegal", back_populates="illegal_pics", foreign_keys="Illegal_pic.illegalid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Employee_base(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(50))
    login_user = db.Column(db.String(50))
    departid = db.Column(db.Integer,db.ForeignKey("depart.id"), nullable= False)
    depart = db.relationship("Depart", back_populates="employees", foreign_keys="Employee.departid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Company_base(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50))
    gongdi = db.relationship("Gongdi", back_populates = "company",uselist=False, foreign_keys="Gongdi.companyid")
    departs = db.relationship("Depart", back_populates="company", foreign_keys="Depart.companyid", cascade="all, delete-orphan")
    dantis = db.relationship("Danti", back_populates="company", foreign_keys="Danti.companyid", cascade="all, delete-orphan")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Company_auth_base(db.Model):
    __tablename__ = 'company_auth'
    id = db.Column(db.Integer, primary_key=True)
    appuserid = db.Column(db.String(50))
    companyid = db.Column(db.Integer,db.ForeignKey("company.id"), nullable= False)
    company = db.relationship("Company", foreign_keys="Company_auth.companyid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Depart_base(db.Model):
    __tablename__ = 'depart'
    id = db.Column(db.Integer, primary_key=True)
    companyid = db.Column(db.Integer,db.ForeignKey("company.id"), nullable= False)
    employees = db.relationship("Employee", back_populates="depart", foreign_keys="Employee.departid", cascade="all, delete-orphan")
    company = db.relationship("Company", back_populates="departs", foreign_keys="Depart.companyid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Quality_inspect(Inspect):
    __mapper_args__ = {'polymorphic_identity': 'quality_inspect'}
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Safety_inspect(Inspect):
    __mapper_args__ = {'polymorphic_identity': 'safety_inspect'}
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Produce_inspect(Inspect):
    __mapper_args__ = {'polymorphic_identity': 'produce_inspect'}
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Inspect_pic_base(db.Model):
    __tablename__ = 'inspect_pic'
    file_name = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)
    pic_size = db.Column(db.Float)
    save_file_name = db.Column(db.String(250))
    inspectid = db.Column(db.Integer,db.ForeignKey("inspect.id"), nullable= False)
    inspect = db.relationship("Inspect", back_populates="inspect_pics", foreign_keys="Inspect_pic.inspectid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Gongdi_base(db.Model):
    __tablename__ = 'gongdi'
    code = db.Column(db.String(50))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    starttime = db.Column(db.Date)
    complete_time = db.Column(db.Date)
    build_unit = db.Column(db.String(50))
    design_unit = db.Column(db.String(50))
    monitor_unit = db.Column(db.String(50))
    construct_unit = db.Column(db.String(50))
    description = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)
    companyid = db.Column(db.Integer,db.ForeignKey("company.id"), nullable= False)
    company = db.relationship("Company", back_populates="gongdi", foreign_keys="Gongdi.companyid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Danti(Buwei):
    __mapper_args__ = {'polymorphic_identity': 'danti'}
    build_type = db.Column(db.String(50))
    framework_type = db.Column(db.String(50))
    dt_area = db.Column(db.String(50))
    dt_plies_num = db.Column(db.String(50))
    eaves_height = db.Column(db.String(50))
    build_schedule = db.Column(db.String(50))
    companyid = db.Column(db.Integer,db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="dantis", foreign_keys="Danti.companyid")
    buweis = db.relationship("Buwei", back_populates="danti", foreign_keys="Buwei.dantiid", cascade="all, delete-orphan")
    def to_jsonex(self):
        data = self.to_json()
        data['comp_name']=self.company.company_name if self.company else ''
        return data
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Doc_file_base(db.Model):
    __tablename__ = 'doc_file'
    file_name = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)
    file_size = db.Column(db.Float)
    save_file_name = db.Column(db.String(250))
    docid = db.Column(db.Integer,db.ForeignKey("doc.id"), nullable= False)
    doc = db.relationship("Doc", back_populates="doc_files", foreign_keys="Doc_file.docid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Guifang_doc(Doc):
    __mapper_args__ = {'polymorphic_identity': 'guifang_doc'}
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Tuzhi_doc(Doc):
    __mapper_args__ = {'polymorphic_identity': 'tuzhi_doc'}
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Tuji_doc(Doc):
    __mapper_args__ = {'polymorphic_identity': 'tuji_doc'}
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Jiaodi_doc(Doc):
    __mapper_args__ = {'polymorphic_identity': 'jiaodi_doc'}
    shigong_danwei = db.Column(db.String(50))
    jiaodi_ren = db.Column(db.String(50))
    bei_jiaodi_ren = db.Column(db.String(50))
    jiaodi_time = db.Column(db.DateTime)
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
