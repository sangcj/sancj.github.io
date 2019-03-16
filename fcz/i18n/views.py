from django.http import HttpResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _


def test(request):
    # user_language = 'zh-Hans'
    user_language = request.GET.get('lang_code', 'en')
    translation.activate(user_language)
    output = _("Welcome to b")
    return HttpResponse(output)


def hello(request):
    user_language = request.GET.get('lang_code', 'en')
    translation.activate(user_language)
    return render(request, 'hello.html', {})
