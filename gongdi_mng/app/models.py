########################################
# create by :cxh-PC
# create time :2018-03-02 15:55:23.154176
########################################
from .models_base import *
class Employee(Employee_base):
    pass
class Illegal_category(Illegal_category_base):
    pass
class Illegal_type(Illegal_type_base):
    def to_json(self):
        data = super().to_json()
        data['illegal_category_name']=self.illegal_category.name
        return data
class Company(Company_base):
    pass
class Subcontractor(Subcontractor_base):
    pass
class Illegal_pic(Illegal_pic_base):
    def to_json(self):
        return {'id':self.id,
                'file_name':self.file_name,
                'pic_size':self.pic_size,
                'illegalid':self.illegalid}
class Company_auth(Company_auth_base):
    pass
class Depart(Depart_base):
    pass
class Inspect_pic(Inspect_pic_base):
    pass
class Gongdi(Gongdi_base):
    def to_json(self):
        data = super().to_json()
        data['comp_name'] = self.company.company_name
        return data
class Doc_file(Doc_file_base):
    def to_json(self):
        data = super().to_json()
        data.pop('save_file_name')
        return data
