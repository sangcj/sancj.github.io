from django import forms

from blogback.models import User


class UserForm(forms.Form):
    username = forms.CharField(max_length=10,
                               required=True,
                               error_messages={
                                   'required': '姓名字段必填',
                                   'max_length': '不能超过10个字符',
                               })
    password1 = forms.CharField(required=True,
                                error_messages={
                                    'required': '密码必填'
                                })


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=30,
                            required=True,
                            error_messages={
                                'required': '标题不能为空',
                                'max_length': '标题长度不能超过30个字符'
                            })

    desc = forms.CharField(max_length=100,
                           required=True,
                           error_messages={
                               'required': '描述不能为空',
                               'max_length': '描述不能超过100个字符'
                           })


# class ArticleType(forms.Form):
#     name = forms.CharField(max_length=10, )