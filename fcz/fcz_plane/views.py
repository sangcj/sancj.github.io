import datetime
from collections import Counter

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET

from fcz.settings import ALL_HOT_AIRPORTS
from fcz_plane.models import CdPlane


def cd_plane(request):
    """
    成都
    :param request:
    :return:
    """
    # return render(request, 'index.html')
    # address = [a.job_location.split(' ')[0] for a in job_all]
    # result_address = dict(Counter(address))  # 工作区域地址
    # info_list = [{'value': j, 'name': i} for i, j in result_address.items()]
    # return render(request, 'map-polygon.html', {'all_list': info_list})

    all_planes = CdPlane.objects.all()
    flightdict = dict(Counter([plane.to_dict()['flightarr'] for plane in all_planes]))
    print(flightdict)
    all_info_list = []
    for name in flightdict.keys():
        if name not in ['香港', '澳门', '台北', '林芝']:
            dict1 = {'name': name, 'value': flightdict[name]//10}
            all_info_list.append(dict1)
    print(all_info_list)
    return render(request, 'plane.html', {'all_dict': all_info_list})

    # return render(request, 'plane.html')


@require_POST
def search(request):
    """
    返回详情信息
    :param request:
    :return:
    """
    date = request.POST.get('time')
    # dep = ALL_HOT_AIRPORTS[request.POST.get('dep')]
    arr = ALL_HOT_AIRPORTS[request.POST.get('arr')]

    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    all_planes = CdPlane.objects.filter(Q(flightarrcode=arr), Q(flightdeptimeplandate__startswith=date))
    all_list = [plane.to_all_dict() for plane in all_planes]
    return JsonResponse({'code': 200, 'data': all_list})


@require_GET
def search_info(request):
    """
    返回详情信息
    :param request:
    :return:
    """
    # return render(request, 'index.html')
    return render(request, 'show_info.html')