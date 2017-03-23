import os

DEBUG = int(os.environ.get('DEBUG', 0)) == 1

SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'tep9tfK93nMs6Nn2Y1MBpIz5c6axT68tfqolYmVMz/8=')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 模板及静态文件目录
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')

# 数据库连接
DATABASE = {
    'USERNAME': os.getenv('DB_USER', 'root'),
    'PASSWORD': os.getenv('DB_PASSWORD', ''),
    'HOST': os.getenv('DB_HOST', '127.0.0.1'),
    'DB': os.getenv('DB', 'aio_todo'),
}
