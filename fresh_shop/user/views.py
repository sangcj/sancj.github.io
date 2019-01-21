from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from fresh_shop.settings import ORDER_NUMBER
from goods.models import Goods
from order.models import OrderInfo
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 使用表单form做校验
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 账号不存在于数据库，密码和确认密码一致，邮箱格式正确
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['cpwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username,
                                password=password,
                                email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 获取表单验证不通过的错误信息
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 用户存在，密码相同
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        # 1
        # request.session.flush()
        # 2.删除对应id
        del request.session['user_id']
        # 删除商品信息
        if request.session.get('goods'):
            del request.session['goods']
        # if request.session.get('all_history_goods'):
        #     del request.session['all_history_goods']
        if request.session.get('user_history'):
            del request.session['user_history']
        return HttpResponseRedirect(reverse('goods:index'))


def user_center_info(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        all_history_goods_id = request.session.get(str(user_id) + 'all_history_goods', 0)
        if all_history_goods_id:
            all_history_goods = [Goods.objects.filter(pk=i).first() for i in all_history_goods_id][:5]
        else:
            all_history_goods = 0
        return render(request, 'user_center_info.html', {'all_history_goods': all_history_goods})


def user_center_order(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        # 获取登陆系统用户id
        user_id = request.session.get('user_id')
        # 查询当前用户所有订单信息
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        return render(request, 'user_center_order.html', {'orders': orders, 'status': status})


def user_center_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        return render(request, 'user_center_site.html', {'user_address': user_address})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address=address,
                                       signer_name=username,
                                       signer_postcode=postcode,
                                       signer_mobile=mobile)
            return HttpResponseRedirect(reverse('user:user_center_site'))
        else:
            errors = form.errors
            return render(request, 'user_center_site.html', {'errors': errors})


# def user_cookies(request):
#     if request.method == 'POST':
#         usr_id = request.session.get('user_id')
#         goods_id = request.POST.get('goods_id')
#         return JsonResponse({'code': 200, 'msg': '请求成功'})
