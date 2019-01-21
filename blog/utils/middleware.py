import time
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

# 定义中间件
from blogback.models import User


# 获取处理日志的logger
logger = logging.getLogger(__name__)


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        if path in ['/blogback/register/', '/blogback/login/']:
            return None
        try:
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            request.user = user
            return None
        except Exception as e:
            return HttpResponseRedirect(reverse('blogback:login'))

    def process_view(self, request, view_func, view_args, view_kyargs):
        pass

    # 执行视图函数后返回前再执行process_response
    def process_response(self, request, response):
        return response


class LoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):

        request.init_time = time.time()

    def process_response(self, request, response):
        try:
            # 请求到响应之间消耗时长
            count_times = time.time() - request.init_time
            # 请求地址和请求方式
            path = request.path
            method = request.method
            # 响应状态码,和内容
            status = response.status_code
            content = response.content
            # 日志记录的信息
            message = '%s %s %s %s %s' % (path, method, status, content, count_times)
            logger.info(message)
        except Exception as e:
            logger.critical('log error:%s' % e)

        return response
