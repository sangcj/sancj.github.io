from flask import session, redirect, url_for


def login_required(func):
    def check(*args, **kwargs):
        if 'user_id' in session:
            # 判断session中是否存在登录的标识user_id
            return func(*args, **kwargs)
        else:
            # 没登陆，跳转到登录
            return redirect(url_for('user.login'))
    return check
