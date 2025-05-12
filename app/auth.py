from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models import db, AdminUser
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/brewmaster-secret')

@auth_bp.before_app_request
def set_session_lifetime():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(hours=18)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if 'admin_user_id' in session:
        return redirect(url_for('main.admin_panel'))

    login_value = request.form.get('login', '')

    if request.method == 'POST':
        password = request.form.get('password', '')
        user = AdminUser.query.filter_by(login=login_value).first()

        if user and user.check_password(password):
            session['admin_user_id'] = user.id

            if user.position_id == 1:
                return redirect(url_for('main.admin_panel'))
            elif user.position_id == 2:
                return redirect(url_for('main.reservation'))

            flash('Недопустимая роль пользователя', 'error')
            return redirect(url_for('auth.login'))

        flash('Неверный логин или пароль', 'error')

    return render_template('login.html', login_value=login_value)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))
