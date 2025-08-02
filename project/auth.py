import json
from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

def load_admin_accounts():
    """加载管理员账户信息。"""
    try:
        with open(current_app.config['ADMIN_FILE'], 'r') as f:
            data = json.load(f)
            return data.get('admins', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        current_app.logger.error(f"Error loading admin accounts: {e}")
        return []

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """处理用户登录请求。"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        error = None

        admin_accounts = load_admin_accounts()
        user = next((admin for admin in admin_accounts if admin['username'] == username), None)

        if user is None or user['password'] != password:
            error = '用户名或密码不正确。'
        
        if error is None:
            session.clear()
            session['user_id'] = user['username']
            session['display_name'] = user.get('display_name', user['username'])
            session['role'] = user.get('role', 'editor')
            session.permanent = remember
            
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.admin'))

        flash(error, 'danger')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """处理用户登出请求。"""
    session.clear()
    flash('您已成功登出。', 'success')
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    """在每个请求前加载已登录的用户信息。"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = {
            'username': user_id,
            'display_name': session.get('display_name'),
            'role': session.get('role')
        }

def login_required(view):
    """一个装饰器，用于保护需要登录才能访问的视图。"""
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('请先登录以访问此页面。', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view
