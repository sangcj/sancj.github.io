from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from blogback.models import User, Article, ArticleType
from blogback.forms import UserForm, ArticleForm


def article(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        all_article = Article.objects.all()
        pg = Paginator(all_article, 6)
        articles = pg.page(page)
        return render(request, 'blogback/article.html', {'article': articles})


def category(request):
    if request.method == 'GET':
        article_type = ArticleType.objects.all()
        return render(request, 'blogback/category.html', {'article_type': article_type})
    if request.method == 'POST':
        name = request.POST.get('name')
        ArticleType.objects.create(t_name=name)
        article_type = ArticleType.objects.all()
        return render(request, 'blogback/category.html', {'msg': '添加成功。', 'article_type': article_type})


def add_article(request):
    if request.method == 'GET':
        return render(request, 'blogback/add-article.html')
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data['title']
            desc = article_form.cleaned_data['desc']
            content = request.POST.get('content', '未编辑内容')
            Article.objects.create(title=title, desc=desc, content=content, t_name_id=1)
            return HttpResponseRedirect(reverse('blogback:article'))
        else:
            errors = article_form.errors
            return render(request, 'blogback/add-article.html', {'errors': errors})


def index(request):
    return render(request, 'blogback/index.html')


def register(request, id):
    if request.method == 'GET':
        if id == 888:
            return render(request, 'blogback/register.html')
        else:
            return HttpResponseRedirect(reverse('blogback:login'))
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password1 = request.POST.get('password1')
        # password2 = request.POST.get('password2')
        # if User.objects.filter(username=username).exists():
        #     msg = '该用户名已存在'
        #     return render(request, 'blogback/register.html', {'msg': msg})
        # if password1 != password2:
        #     msg = '密码不一致'
        #     return render(request, 'blogback/register.html', {'msg': msg})
        # password = make_password(password1)
        # User.objects.create(username=username, password=password)
        # return HttpResponseRedirect(reverse('blogback/login'))

        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password = make_password(password1)
            User.objects.create(username=username, password=password)
            return HttpResponseRedirect(reverse('blogback:login'))
        else:
            errors = form.errors
            return render(request, 'blogback/register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'blogback/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        user = User.objects.filter(username=username).first()
        if user:
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('blogback:index'))
            else:
                msg = '密码错误'
                return render(request, 'blogback/login.html', {'msg': msg})
        else:
            msg = '不存在该用户'
            return render(request, 'blogback/login.html', {'msg': msg})


def update_article(request, id):
    if request.method == 'GET':
        article1 = Article.objects.filter(pk=id).first()
        return render(request, 'blogback/update-article.html', {'article': article1})
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        desc = request.POST.get('desc')
        # article2 = Article.objects.filter(pk=id).first()
        # article2.title = title
        # article2.content = content
        # article2.desc = desc
        # article2.save()
        Article.objects.filter(pk=id).update(title=title, content=content, desc=desc)
        return HttpResponseRedirect(reverse('blogback:article'))


def delete_article(request, id):
    Article.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse('blogback:article'))



