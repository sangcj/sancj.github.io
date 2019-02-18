import os
import random
import re
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

# from aj.forms import MyForm, RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user

# from aj.forms import RegisterForm, LoginForm
from aj.models import Order, User, House, Area

login_manage = LoginManager()
user = Blueprint('user', __name__)

# 设置校验失败跳转页面
login_manage.login_view = "/"


@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user.route('/login/', methods=['POST'])
def my_login():
    # 实现登录
    mobile = request.form.get('mobile')
    passwd = request.form.get('passwd')
    # 1.校验参数是否填写完整
    if not all([mobile, passwd]):
        return jsonify({'code': 1006, 'msg': '请填写完整'})

    if not re.match(r"^1[3456789]\d{9}$", mobile):
        return jsonify({'code': 1007, 'msg': '手机号不正确'})
    # 2.获取手机号对应的用户信息
    user = User.query.filter_by(phone=mobile).first()
    if not user:
        return jsonify({'code': 1008, 'msg': '该账号未注册，请先注册'})
    else:
        # 3.校验密码是否正确
        if not user.check_pwd(passwd):
            return jsonify({'code': 1009, 'msg': '账号密码不匹配，请重新输入'})
    # 4.登录标识设置
    # session['user_id'] = user.id
    # 4.flask-login
    login_user(user)
    return jsonify({'code': 200, 'msg': '请求成功'})


@login_manage.user_loader
def load_user(user_id):
    # 定义被login_manage装饰的回调函数
    # 返回的是当前登录系统的用户对象
    return User.query.filter(User.id == user_id).first()


# 前端的工作
@user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


# 后端的
@user.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    # if not(mobile and passwd and passwd2 and imagecode):
    #     return jsonify({'code': 403, 'msg': '数据有误'})

    # all(list1):结果为布尔值，如果list1中有一个元素为空
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整参数'})

    # 2.验证手机号正确
    re_mobile = re.match(r"^1[3456789]\d{9}$", mobile)
    if not re_mobile:
        return jsonify({'code': 1002, 'msg': '手机号不正确'})

    # 3.验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码不正确'})

    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '密码不一致'})

    # 验证手机号是否已注册
    if User.query.filter(User.phone == mobile).first():
        return jsonify({'code': 1005, 'msg': '该手机号已被注册，请重新注册'})

    # 创建注册信息
    user = User()
    user.password = passwd
    user.phone = mobile
    user.name = mobile
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


# 获取验证码
@user.route('/code/', methods=['GET'])
def get_code():
    # 方式一：后端生成图片，并返回验证码图片的地址（不推荐）
    # 方式二：后端只生成随机参数，返回给页面，在页面中生成图片
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    code = ''
    for i in range(4):
        code += random.choice(s)
    # 存储验证码
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


@user.route('/user_info/', methods=['GET'])
def user_info():
    # 获取用户信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    # user.to_basic_dict() 利用对象方法转化为json数据
    if user.id_card:
        # area_list = [[area.id, area.name] for area in Area.query.all()]
        houses = House.query.all()
        houses_list = [house.to_dict() for house in houses]
        return jsonify({'code': 1014, 'msg': '当前用户已实名注册',
                        'authData': user.to_auth_dict(), 'data': user.to_basic_dict(),
                        'houses_list': houses_list})
    return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


@user.route('/name_profile/', methods=['POST'])
def name_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    new_name = request.form.get('new_name')
    if not new_name:
        return jsonify({'code': 1012, 'msg': '姓名不能为空，请重新输入'})
    if User.query.filter_by(name=new_name).first():
        return jsonify({'code': 1011, 'msg': '该用户名已被注册，请重新输入'})
    user.name = new_name
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user.route('/profile/', methods=['PATCH'])
def my_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    avatar = request.files.get('avatar')
    if avatar:
        # abspath绝对路径
        # 当前文件user_views.py的绝对路径os.path.abspath(__file__)
        # 上一层路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
        # 随机生成名称
        avatar_name = str(uuid.uuid4())
        # 获取图片格式
        g = avatar.mimetype.split('/')[-1:][0]
        # 拼接唯一名字
        name = avatar_name + '.' + g
        # 拼接地址
        avatar_path = os.path.join(MEDIA_DIR, name)
        avatar.save(avatar_path)
        user.avatar = name
        user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})
    else:
        return jsonify({'code': 1010, 'msg': '上传图片不能为空'})


@user.route('/orders/', methods=['GET'])
def orders():
    user_id = session.get('user_id')
    all_my_orders = Order.query.filter(Order.user_id == user_id).all()
    all_my_orders_image = []
    for my_orders in all_my_orders:
        all_my_orders_image.append([my_orders, House.query.filter_by(id=my_orders.house_id).first().index_image_url])
    order_status = [["WAIT_ACCEPT", "待接单"], ["WAIT_PAYMENT", "待支付"], ["PAID", "已支付"], ["WAIT_COMMENT", "待评价"],
                    ["COMPLETE", "已完成"], ["CANCELED", "已取消"], ["REJECTED", "已拒单"]]
    return render_template('orders.html', all_my_orders=all_my_orders_image, order_status=order_status)


@user.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@user.route('/auth/', methods=['POST'])
def my_auth():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_id_name = request.form.get('id_name')
    user_id_card = request.form.get('id_card')
    if not all([user_id_card, user_id_name]):
        return jsonify({'code': 1016, 'msg': '输入内容不能为空'})
    if User.query.filter_by(id_card=user_id_card).first():
        return jsonify({'code': 1015, 'msg': '该身份证号码已被注册，请重新输入'})
    user.id_name = user_id_name
    user.id_card = user_id_card
    user.add_update()
    return jsonify({'code': 200, 'msg': '认证成功', 'authData': user.to_auth_dict()})


@user.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')
    # my_houses = House.query.all()
    # area_list = [[area.id, area.name] for area in Area.query.all()]
    # return render_template('myhouse.html', my_houses=my_houses, area_list=area_list)


@user.route('/lorders/', methods=['GET'])
def lorders():
    user_id = session.get('user_id')
    houses = House.query.filter(House.user_id == user_id).all()
    customer_order = []
    for house in houses:
        c_order = Order.query.filter(Order.house_id == house.id).all()
        customer_order += c_order
    order_status = [["WAIT_ACCEPT", "待接单"], ["WAIT_PAYMENT", "待支付"], ["PAID", "已支付"], ["WAIT_COMMENT", "待评价"],
                    ["COMPLETE", "已完成"], ["CANCELED", "已取消"], ["REJECTED", "已拒单"]]
    return render_template('lorders.html', customer_order=customer_order, houses=houses, order_status=order_status)


@user.route('/take_order/', methods=['PATCH'])
def take_order():
    # o = request.form.get('order_id')
    order_id = int(request.form.get('order_id'))
    reject_reason = request.form.get('reject_reason')
    status = request.form.get('status')
    order = Order.query.get(order_id)
    if status == 'accept':
        order.status = "WAIT_PAYMENT"
        order.add_update()

    if status == 'reject':
        if not reject_reason:
            return jsonify({'code': 1019, 'msg': '拒单原因不能为空'})
        order.status = "REJECTED"
        order.reject_reason = reject_reason
        order.add_update()

    return jsonify({'code': 200, 'msg': '请求成功'})


@user.route('/booking/<house_id>/', methods=['GET', 'POST'])
@login_required
def booking(house_id):
    house = House.query.get(house_id)
    # house_images = HouseImage.query.filter(HouseImage.house_id == house_id)
    # 房屋所有者
    # user = User.query.filter(User.id == house.user_id).first()
    if request.method == 'GET':
        # return render_template('booking.html', house=house, user=user)
        return render_template('booking.html', house=house)
    if request.method == 'POST':
        # 订单所有者
        user_id = session.get('user_id')
        begin_data = request.form.get('begin_data')
        end_data = request.form.get('end_data')
        days = request.form.get('days')
        house_price = request.form.get('house_price')
        amount = request.form.get('amount')
        comment = request.form.get('comment')

        not_show1 = Order.query.filter(Order.house_id == house_id, begin_data <= Order.begin_date, Order.begin_date <= end_data).all()
        not_show2 = Order.query.filter(Order.house_id == house_id, begin_data <= Order.begin_date, Order.end_date <= end_data).all()
        not_show3 = Order.query.filter(Order.house_id == house_id, begin_data >= Order.begin_date, Order.end_date >= end_data).all()
        not_show4 = Order.query.filter(Order.house_id == house_id, begin_data <= Order.end_date, Order.end_date <= end_data).all()

        if not_show1 + not_show2 + not_show3 + not_show4:
            return jsonify({'code': 1018, 'msg': '该房间在此时间段内已被预订，请选择合适的时间段。'})

        user_order = Order.query.filter_by(user_id=user_id).all()
        for order in user_order:
            if order.house_id == int(house_id):
                order.begin_date = begin_data
                order.end_date = end_data
                order.days = days
                order.amount = amount
                order.comment = comment
                order.add_update()
                return jsonify({'code': 1017, 'msg': '更新订单成功'})
        order = Order()
        order.user_id = User.query.get(user_id).id
        order.house_id = House.query.get(house_id).id
        order.begin_date = begin_data
        order.end_date = end_data
        order.days = days
        order.house_price = house_price
        order.amount = amount
        order.comment = comment
        # 生成订单号
        order.order_num = str(uuid.uuid4())
        order.add_update()

        # return redirect(url_for('/user/orders/', user_id=user_id))
        return jsonify({'code': 200, 'msg': '创建订单成功'})


@user.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return jsonify({'code': 200, 'msg': '请求成功'})
