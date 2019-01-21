from django.core.paginator import Paginator
from django.shortcuts import render

from blogback.models import Article


# def index(request):
#     if request.method == 'GET':
#         article = Article.objects.all()
#         return render(request, 'blogsec/index.html', {'article': article})
def index(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        all_article = Article.objects.all()
        pg = Paginator(all_article, 6)
        articles = pg.page(page)
        return render(request, 'blogsec/index.html', {'article': articles})


def share(request):
    return render(request, 'blogsec/share.html')


def my_list(request):
    return render(request, 'blogsec/list.html')


def about(request):
    return render(request, 'blogsec/about.html')


def gbook(request):
    return render(request, 'blogsec/gbook.html')


def info(request, id):
    aticle = Article.objects.filter(pk=id).first
    return render(request, 'blogsec/info.html', {'article': aticle})


def infopic(request):
    return render(request, 'blogsec/infopic.html')


def time(request):
    return render(request, 'blogsec/time.html')


def life(request):
    return render(request, 'blogsec/life.html')
