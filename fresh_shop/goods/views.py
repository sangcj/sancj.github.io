from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from goods.models import Goods, GoodsCategory


def index(request):
    if request.method == 'GET':
        # 如果访问首页，返回渲染的首页index.html页面
        # all_goods_category = GoodsCategory.objects.all()
        # list1 = []
        # for goods_category in all_goods_category:
        #     all_goods = Goods.objects.filter(category=goods_category.id)
        #     list2 = [all_goods, goods_category]
        #     list1.append(list2)
        # print(list1)
        # return render(request, 'index.html', {'all_goods': list1})

        # 思路：组装结果
        # 组装结果的对象object：包含分类，该分类的前四个商品信息
        # 方式1：object==>[GoodsCategory Object,[Goods objects1,...]]
        # 方式2：object==>{'category_name':[Goods objects1,...]}
        all_goods_category = GoodsCategory.objects.all()
        result = []
        for goods_category in all_goods_category:
            all_goods = goods_category.goods_set.all()[:4]
            data = [goods_category, all_goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html', {'result': result, 'category_type': category_type})


def detail(request, id):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        # 返回详情页面解析的商品信息
        goods = Goods.objects.filter(pk=id).first()
        goods_category = GoodsCategory.objects.filter(pk=goods.category_id).first()
        category_type = GoodsCategory.CATEGORY_TYPE
        if user_id:
            session_goods = request.session.get('user_history', 0)
            if session_goods:
                for goods_id in session_goods:
                    if goods_id == goods.id:
                        session_goods.remove(goods_id)
                        session_goods.append(goods.id)
                        break
                else:
                    session_goods.append(goods.id)
                # session_goods = request.session.get['user_history']
            else:
                request.session['user_history'] = [goods.id]
                session_goods = request.session.get('user_history')
            all_history_goods = [i for i in session_goods][::-1]
            request.session[str(user_id) + 'all_history_goods'] = all_history_goods
        return render(request, 'detail.html', {'goods': goods, 'goods_category': goods_category,
                                               'category_type': category_type})
    # if request.method == 'POST':
        # data_search_goods = int(request.POST.get('data_search_goods'))
        # data_search_goods = request.POST.get('data_search_goods')
        # s_goods = Goods.objects.filter(id=data_search_goods).first()
        # s_goods_category = GoodsCategory.objects.filter(pk=s_goods.category_id).first()
        # s_category_type = GoodsCategory.CATEGORY_TYPE
        # return HttpResponseRedirect(reverse('user:user_center_order'))
        # return JsonResponse({'code': 200, 'msg': '请求成功', 'data_search_goods': data_search_goods})


def goods_list(request, id):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        goods_category = GoodsCategory.objects.filter(pk=id).first()
        all_goods = goods_category.goods_set.all()
        pg = Paginator(all_goods, 4)
        goods = pg.page(page)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'list.html', {'goods': goods, 'id': id, 'category_type': category_type})


def search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        all_goods = Goods.objects.all()
        for goods in all_goods:
            if goods.name == name:
                search_goods = goods.id
                return JsonResponse({'code': 200, 'search_goods': search_goods})
        else:
            return JsonResponse({'code': 200, 'msg': '未查询到相关内容'})
