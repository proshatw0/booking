from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models import db, AdminUser
from datetime import timedelta

# Blueprint для маршрутов, связанных с аутентификацией
auth_bp = Blueprint('auth', __name__, url_prefix='/brewmaster-secret')

# Устанавливаем срок жизни сессии на 18 часов для всех запросов приложения
@auth_bp.before_app_request
def set_session_lifetime():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(hours=18)

# Маршрут входа в систему (GET — форма входа, POST — попытка входа)
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    # Если пользователь уже в сессии — перенаправляем на нужную панель
    if 'admin_user_id' in session:
        return redirect(url_for('main.admin_panel'))

    login_value = request.form.get('login', '') # сохраняем логин для повторного отображения

    if request.method == 'POST':
        password = request.form.get('password', '')
        user = AdminUser.query.filter_by(login=login_value).first()

        # Проверка пользователя и пароля
        if user and user.check_password(password):
            session['admin_user_id'] = user.id

            # Перенаправление по роли (1 — админ, 2 — хостес)
            if user.position_id == 1:
                return redirect(url_for('main.admin_panel'))
            elif user.position_id == 2:
                return redirect(url_for('main.reservations'))

            flash('Недопустимая роль пользователя', 'error')
            return redirect(url_for('auth.login'))

        flash('Неверный логин или пароль', 'error')

    return render_template('login.html', login_value=login_value)

# Маршрут выхода из системы: очищает сессию и возвращает на форму входа
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))
