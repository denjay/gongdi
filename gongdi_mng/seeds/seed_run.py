from seeds.seed_rm import init_rm_data
from seeds.seed_init import init_default_data
from seeds.seed_dev_data import init_dev_data
from config import is_development
if __name__ == '__main__':
    if is_development:
        init_dev_data()
    init_rm_data('default')
    init_default_data('default')
