########################################
# create by :cxh-pc
# create time :2018-03-16 11:02:38.317254
########################################
'''
python seed_run.py 把资料写入资料库
'''
from seeds.seed_rm import init_rm_data
from seeds.seed_init import init_default_data
from seeds.seed_dev_data import init_dev_data
from config import is_development
if __name__ == '__main__':
    if is_development:
        init_dev_data()
    init_rm_data('default')
    init_default_data('default')
