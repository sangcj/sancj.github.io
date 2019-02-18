from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError, Regexp

from aj.models import User


# class MyForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])
#
#     def validate_name(self, filed):
#         name = filed.data
#         account = User.query.filter(User.phone == name).count()
#         if account == 1:
#             raise ValidationError("昵称已经存在")


class RegisterForm(FlaskForm):
    mobile = StringField('mobile', validators=[DataRequired(), Regexp("1[3578]\d{9}", message="手机格式不正确")],
                         render_kw={'class': 'form-control',
                                    'placeholder': '请输入手机号码',
                                    'value': ''})

    def validate_mobile(self, filed):
        mobile = filed.data
        account = User.query.filter(User.phone == mobile).count()
        if account == 1:
            raise ValidationError("该号码已被注册")


class LoginForm(FlaskForm):
    mobile = StringField('mobile', validators=[DataRequired(), Regexp("1[3578]\d{9}", message="手机格式不正确")],
                         render_kw={'class': 'form-control',
                                    'placeholder': '手机号',
                                    'value': ''})

    # def validate_mobile(self, filed):
    #     mobile = filed.data
    #     user = User.query.filter(User.phone == mobile)
    #     if user and user.check_pwd():
    #         raise ValidationError("该号码已被注册")
