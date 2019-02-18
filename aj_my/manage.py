import os

import redis
from flask import Flask, render_template, jsonify, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session

from aj.house_views import house
from aj.models import db, House, User, Area, Facility
from aj.user_views import user, login_manage

aj = Flask(__name__)

aj.register_blueprint(blueprint=user, url_prefix='/user')
aj.register_blueprint(blueprint=house, url_prefix='/house')

# 设置加密
select_key = os.urandom(24)
aj.select_key = select_key

# 配置flask-session库
aj.config['SESSION_TYPE'] = 'redis'
# aj.config['SESSION_REDIS'] = redis.Redis(host='47.107.124.147', port=6379, password='123123')
aj.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

# 初始化配置
se = Session()
se.init_app(aj)


aj.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/aj1'
aj.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 初始化数据库连接
db.init_app(app=aj)

# 初始化flask-login
login_manage.init_app(aj)

# form表单csrf
aj.config['CSRF_ENABLED'] = True
aj.config['SECRET_KEY'] = 'you-will-never-guess'

manage = Manager(app=aj)

# 使用flask_migrate,需绑定app db
migrate = Migrate(aj, db)
manage.add_command('db', MigrateCommand)


# @aj.before_request
# def is_login():
#     print('12123312')


@aj.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@aj.route('/index/', methods=['GET'])
def my_index():
    houses = House.query.all()[-3:]
    # 利用对象方法组成数据
    # all_house_msg = [house.to_dict() for house in houses]
    all_house_msg = [{'house_id': house.id, 'house_image': house.index_image_url, 'house_title': house.title} for house in houses]
    user_id = session.get('user_id')

    all_area = [area.to_dict() for area in Area.query.all()]
    all_facility = [facility.to_dict() for facility in Facility.query.all()]
    if not user_id:
        return jsonify({'code': 1013, 'msg': '请求成功', 'all_house_msg': all_house_msg, 'area': all_area})
    user = User.query.get(user_id)
    return jsonify({'code': 200, 'msg': '请求成功', 'all_house_msg': all_house_msg,
                    'area': all_area, 'all_facility': all_facility,
                    'user_phone': user.phone})


if __name__ == '__main__':
    manage.run()
