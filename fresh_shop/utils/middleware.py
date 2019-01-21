# import re
#
from django.http import HttpResponseRedirect
# # from django.shortcuts import render
from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin
# #
# from user.models import User
#
#
# class LoginMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#             path = request.path
#             if path in ['/user/register/', '/user/login/']:
#                 return None
#     #         if path in ['/user/register/', '/user/login/', '/goods/index/', '/goods/detail/.*/', '/cart/cart/']:
#     #             try:
#     #                 user_id = request.session['user_id']
#     #                 user = User.objects.get(pk=user_id).first()
#     #                 request.user = user
#     #                 return None
#     #             except Exception as e:
#     #                 return None
#             not_need_check = ['/user/register/', '/user/login/', '/goods/index/', '/goods/detail/.*/', '/cart/.*/']
#             for check_path in not_need_check:
#                 if re.match(check_path, path):
#                     # 当前path路劲为不需要做登陆校验的路由
#                     try:
#                         user_id = request.session['user_id']
#                         user = User.objects.get(pk=user_id)
#                         request.user = user
#                         return None
#                     except Exception as e:
#                         return None
#             try:
#                 user_id = request.session['user_id']
#                 user = User.objects.get(pk=user_id).first
#                 request.user = user
#                 return None
#             except Exception as e:
#                 return HttpResponseRedirect(reverse('user:login'))
#
#     def process_response(self, request, response):
#         return response
import re

from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 拦截请求之前的函数
        # 给request.user属性赋值，赋值为当前登录系统的用户
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
            return None
        # 2.登陆校验，需区分那些地址需要做登录校验，那些地址不需要做登陆校验
        path = request.path
        # 不拦截首页
        if path == '/':
            return None
        not_need_check = ['/user/register/', '/user/login/', '/goods/index/', '/goods/detail/.*/', '/cart/.*/',
                          '/media/.*/', '/static/.*/', '/goods/goods_list/.*/', '/goods/search/.*']
        for check_path in not_need_check:
            if re.match(check_path, path):
                # 当前path路劲为不需要做登陆校验的路由
                return None
        # path为需要做登陆校验的路由时，判断用户是否登陆，没登陆跳转道登陆页面
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))


class SessionToDbMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 同步session中的商品信息和数据库中购物车表的商品信息
        # 1.判断用户是否登陆，登陆才做数据同步
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            # 2.1 判断session中商品是否存在与数据库中存在更新
            # 2.2 不存在创建
            # 2.3 同步数据库数据到session中
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    # se_goods为[goods_id, num, is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                       goods_id=se_goods[0]).first()
                    if cart:
                        # 更新商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums=se_goods[1],
                                                    is_select=se_goods[2])
            # 同步数据库数据到session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            # 组装返回格式：[objects1,objects2...]
            # objects==> [[goods_id, num, is_select],[goods_id, num, is_select]..]
            if db_carts:
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_carts]
                # result = []
                # for cart in db_carts:
                #     data = [cart.goods_id, cart.nums, cart.is_select]
                #     result.append(data)
                request.session['goods'] = new_session_goods
        return response
