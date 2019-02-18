from datetime import datetime
import os
import uuid

from flask import Blueprint, render_template, request, session, jsonify
from sqlalchemy import or_

from aj.models import User, Facility, HouseImage, House, Area, Order

house = Blueprint('house', __name__)


@house.route('/detail/', methods=['GET'])
def detail():
    house_id = request.args.get('house_id')
    house = House.query.get(house_id)
    house_images = HouseImage.query.filter(HouseImage.house_id == house_id)
    user = User.query.filter(User.id == house.user_id).first()

    facilities = house.facilities
    return render_template('detail.html', house=house, house_images=house_images, user=user, facilities=facilities)


@house.route('/detail_info/', methods=['POST'])
def my_detail():
    house_id = request.form.get('house_id')
    house = House.query.get(house_id)
    # house_images = HouseImage.query.filter(HouseImage.house_id == house_id)
    user = User.query.filter(User.id == house.user_id).first()

    # facilities = house.facilities
    # return render_template('detail.html', house=house, house_images=house_images, user=user, facilities=facilities)
    return jsonify({'code': 200, 'house': house.to_full_dict(), 'user': user.to_basic_dict()})


# @house.route('/my/', methods=['GET'])
# def my():
#     return render_template('my.html')


@house.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@house.route('/newhouse/', methods=['POST'])
def my_newhouse():
    user_id = session.get('user_id')
    house = House()
    user1 = User.query.get(user_id)
    house.user_id = user1.id
    house.title = request.form.get('title')
    house.price = request.form.get('price')
    # 房屋所在城区编号
    area1 = Area.query.get(int(request.form.get('area_id')))
    house.area_id = area1.id
    house.address = request.form.get('address')
    # 出租房间数目
    house.room_count = request.form.get('room_count')
    # 房屋面积
    house.acreage = request.form.get('acreage')
    # 户型描述
    house.unit = request.form.get('unit')
    # 适宜居住人数
    house.capacity = request.form.get('capacity')
    # 卧床配置
    house.beds = request.form.get('beds')
    # 房屋押金
    house.deposit = request.form.get('deposit')
    # 最少入住天数
    house.min_days = request.form.get('min_days')
    # 最多入住天数，为0表示不限制
    house.max_days = request.form.get('max_days')
    # 房屋主图片
    # 获取多个图片对象
    # house_images = request.form.getlist('house_image')[0]
    house_images = request.files.getlist('house_image')
    if not house_images:
        return jsonify({'code': 1016, 'msg': '上传图片不能为空!'})
    # house_images = request.files.get('house_image')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    IMAGES = os.path.join(STATIC_DIR, 'images')
    for index in range(0, len(house_images)):
        # 随机生成名称
        image_name = str(uuid.uuid4())
        # 获取图片格式
        g = house_images[index].mimetype.split('/')[-1:][0]
        # 拼接唯一名字
        name = image_name + '.' + g
        # 拼接地址
        image_path = os.path.join(IMAGES, name)
        house_images[index].save(image_path)
        if index == 0:
            house.index_image_url = name
            house.add_update()
        # 房屋照片
        ihome_house_images = HouseImage()
        ihome_house_images.house_id = house.id
        ihome_house_images.url = name
        ihome_house_images.add_update()
    # id = house.id
    # print('1212')
    # 房屋设施
    facilities = request.form.getlist('facility')
    for f_id in facilities:
        facility = Facility.query.get(int(f_id))
        house.facilities.append(facility)
        house.add_update()

    return jsonify({'code': 200, 'msg': '请求成功'})


@house.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@house.route('/search/', methods=['POST'])
def my_search():
    sd = datetime.strptime(request.form.get('startDate'), '%Y-%m-%d')
    ed = datetime.strptime(request.form.get('endDate'), '%Y-%m-%d')
    days = (ed - sd).days + 1
    area_id = request.form.get('areaId')

    # 排除不同地区,及出租天数不满足条件的房源
    # houses = House.query.filter(House.area_id == area_id, House.min_days <= days,
    #                             (days <= House.max_days if House.max_days else True)).all()

    houses = House.query.filter(House.area_id == area_id, House.min_days <= days,
                                or_(House.max_days == 0, days <= House.max_days)).all()

    # 筛选不满足条件的房源
    not_show1 = Order.query.filter(sd <= Order.begin_date, Order.begin_date <= ed).all()
    not_show2 = Order.query.filter(sd <= Order.begin_date, Order.end_date <= ed).all()
    not_show3 = Order.query.filter(sd >= Order.begin_date, Order.end_date >= ed).all()
    not_show4 = Order.query.filter(sd <= Order.end_date, Order.end_date <= ed).all()

    not_show = list(set(not_show1+not_show2+not_show3+not_show4))
    not_show_house = [order.house for order in not_show]

    houses_info = [[t_house.to_dict(), t_house.user.to_basic_dict()] for t_house in houses if t_house not in not_show_house]

    return jsonify({'code': 200, 'msg': '请求成功', 'houses_info': houses_info})


# 创建设施表
@house.route('/creat_facilities/', methods=['GET'])
def creat_facilities():
    facilities_name = ['无线网络', '热水淋浴', '空调', '暖气', '允许吸烟', '饮水设备', '牙具', '香皂', '拖鞋', '手纸',
                       '毛巾', '沐浴露、洗发露', '冰箱', '洗衣机', '电梯', '允许做饭', '允许带宠物', '允许聚会', '门禁系统'
                       , '停车位', '有线网络', '电视', '浴缸']
    facilities_css = ["wirelessnetwork-ico", "shower-ico", "aircondition-ico", "heater-ico", "smoke-ico", "drinking-ico",
                      "brush-ico", "soap-ico", "slippers-ico", "toiletpaper-ico", "towel-ico", "toiletries-ico",
                      "icebox-ico", "washer-ico", "elevator-ico", "iscook-ico", "pet-ico", "meet-ico", "accesssys-ico",
                      "parkingspace-ico", "wirednetwork-ico", "tv-ico", "jinzhi-ico"]
    for id in range(1, 24):
        # print(id)
        facility = Facility()
        facility.id = id
        facility.name = facilities_name[id-1]
        facility.css = facilities_css[id-1]
        facility.add_update()
    return render_template('newhouse.html')


# 创建城区表
@house.route('/creat_area/', methods=['GET'])
def creat_area():
    id = 1
    area_name = ['东城区', '西城区', '朝阳区', '海淀区', '昌平区', '丰台区','房山区', '通州区', '顺义区', '大兴区',
                 '怀柔区', '平谷区', '密云区', '延庆区', '石景山区', '门头沟区']
    for name in area_name:
        area = Area()
        area.id = id
        area.name = name
        area.add_update()
        id += 1
    return render_template('newhouse.html')