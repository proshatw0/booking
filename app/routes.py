import os
from flask import send_file, Blueprint, request, redirect, url_for, render_template, flash, current_app, session, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from io import BytesIO
from app import db
from app.models import Table, AdminUser, Position, Status, Reservation
from datetime import datetime, time
from sqlalchemy import and_, or_
import pytz

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/tables', methods=['GET'])
def list_tables():
    tables = Table.query.order_by(Table.name).all()
    return render_template('tables_list.html', tables=tables)

@main_bp.route('/edit_table/<int:table_id>', methods=['GET', 'POST'])
def edit_table(table_id):
    table = Table.query.get_or_404(table_id)

    if request.method == 'POST':
        table.name = request.form['name']
        table.description = request.form['description']
        table.capacity = request.form['capacity']
        table.deposit = request.form.get('deposit', type=float)

        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(new_photo_path)

            if table.photo and os.path.exists(table.photo):
                os.remove(table.photo)

            table.photo = new_photo_path

        db.session.commit()
        flash('Стол успешно обновлён!', 'success')
        return redirect(url_for('main.list_tables'))

    return render_template('edit_table.html', table=table)

@main_bp.route('/add_table', methods=['GET', 'POST'])
def add_table():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        capacity = request.form['capacity']
        deposit = request.form.get('deposit', type=float)

        photo_path = None
        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(photo_path)

        new_table = Table(name=name, description=description, capacity=capacity, deposit=deposit, photo=photo_path)
        db.session.add(new_table)
        db.session.commit()

        flash('Новый стол успешно добавлен!', 'success')
        return redirect(url_for('main.list_tables'))

    return render_template('add_table.html')



@main_bp.route('/brewmaster-secret/panel/')
def admin_panel():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    if user.position_id == 2:
        return redirect(url_for('main.reservations'))

    return render_template('panel.html')

@main_bp.route('/brewmaster-secret/staff/')
def admin_staff():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    if user.position_id == 2:
        return redirect(url_for('main.reservations'))

    staff_users = AdminUser.query.all()
    positions = Position.query.all()
    return render_template('staff.html', staff_users=staff_users, positions=positions)

@main_bp.route('/brewmaster-secret/reservations/')
def reservations():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    reservations = Reservation.query.order_by(Reservation.date.asc(), Reservation.start_time.asc()).all()
    return render_template('reservations.html', reservations=reservations)

@main_bp.route('/brewmaster-secret/reservations/filter')
def filter_reservations():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401

    date = request.args.get('filter_date')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    search_query = request.args.get('search_query')

    query = Reservation.query.join(Table)

    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(Reservation.date == date_obj)
        except ValueError:
            pass

    if start_time:
        try:
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()
            query = query.filter(Reservation.start_time >= start_time_obj)
        except ValueError:
            pass

    if end_time:
        try:
            end_time_obj = datetime.strptime(end_time, "%H:%M").time()
            query = query.filter(Reservation.end_time <= end_time_obj)
        except ValueError:
            pass

    if search_query:
        search = f"%{search_query.strip().lower()}%"
        query = query.filter(
            db.or_(
                db.func.lower(Reservation.name).like(search),
                db.func.lower(Reservation.special_requests).like(search),
                db.func.lower(Table.name).like(search)
            )
        )

    reservations = query.order_by(Reservation.date.asc(), Reservation.start_time.asc()).all()

    return jsonify([
        {
            'id': r.id,
            'name': r.name,
            'status': r.status.name,
            'date': r.date.strftime('%d.%m.%Y'),
            'start_time': r.start_time.strftime('%H:%M'),
            'end_time': r.end_time.strftime('%H:%M'),
            'num_people': r.num_people,
            'table_name': r.table.name
        }
        for r in reservations
    ])

@main_bp.route('/brewmaster-secret/reservations/add', methods=['POST'])
def add_reservations():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    name = request.form.get('name')
    date = request.form.get('date')
    start_time = request.form.get('time_from')
    end_time = request.form.get('time_to')
    num_people = request.form.get('people_count')
    phone = request.form.get('phone')
    email = request.form.get('email')
    special_requests = request.form.get('notes')

    try:
        date = datetime.strptime(date, "%Y-%m-%d") 
    except ValueError:
        flash('Неверный формат даты', 'error')
        return redirect(url_for('main.reservations'))

    try:
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        table_id = int(request.form.get('table'))
    except ValueError:
        flash('Неверный формат данных', 'error')
        return redirect(url_for('main.reservations'))

    table = Table.query.get(table_id)
    if not table:
        flash('Указанный стол не существует', 'error')
        return redirect(url_for('main.reservations'))

    reservation = Reservation(
        name=name,
        status_id=1,
        date=date,
        start_time=start_time,
        end_time=end_time,
        table_id=table_id,
        num_people=num_people,
        phone=phone,
        email=email,
        special_requests=special_requests,
        admin_user_id=admin_id
    )

    db.session.add(reservation)
    db.session.commit()

    flash('Бронь успешно добавлена', 'success')
    return redirect(url_for('main.reservations'))

@main_bp.route('/brewmaster-secret/reservations/edit/<int:reservation_id>', methods=['GET'])
def edit_reservation(reservation_id):
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    reservation = Reservation.query.get_or_404(reservation_id)
    statuses = Status.query.all()

    admin_user = reservation.admin_user
    if admin_user:
        responsible = f"{admin_user.last_name} {admin_user.first_name[0]}.{admin_user.middle_name[0]}." if admin_user.middle_name else f"{admin_user.last_name} {admin_user.first_name[0]}."
    else:
        responsible = None

    return jsonify({
        'id': reservation.id,
        'name': reservation.name,
        'date': reservation.date.strftime('%Y-%m-%d'),
        'start_time': reservation.start_time.strftime('%H:%M'),
        'end_time': reservation.end_time.strftime('%H:%M'),
        'table_number': reservation.table_id,
        'num_people': reservation.num_people,
        'phone': reservation.phone,
        'email': reservation.email,
        'special_requests': reservation.special_requests,
        'status_id': reservation.status_id,
        'status_name': reservation.status.name,
        'created_at': reservation.created_at.strftime('%d.%m.%Y %H:%M'),
        'responsible': responsible,
        'statuses': [{'id': s.id, 'name': s.name} for s in statuses]
    })

@main_bp.route('/brewmaster-secret/reservations/update', methods=['POST'])
def update_reservation():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    reservation_id = request.form.get('reservation_id')
    reservation = Reservation.query.get_or_404(reservation_id)

    table = Table.query.get(int(request.form['table_edit']))
    if not table:
        flash('Указанный стол не существует', 'error')
        return redirect(url_for('main.reservations'))

    try:
        reservation.name = request.form['name_edit']
        reservation.date = datetime.strptime(request.form['date_edit'], "%Y-%m-%d")
        reservation.start_time = datetime.strptime(request.form['time_from_edit'], "%H:%M").time()
        reservation.end_time = datetime.strptime(request.form['time_to_edit'], "%H:%M").time()
        reservation.table_id = int(request.form['table_edit'])
        reservation.num_people = int(request.form['people_count_edit'])
        reservation.phone = request.form['phone_edit']
        reservation.email = request.form['email_edit']
        reservation.special_requests = request.form['notes_edit']
        reservation.status_id = int(request.form['status_edit'])

        db.session.commit()
        flash('Бронь успешно обновлена', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при обновлении брони: {str(e)}', 'error')

    return redirect(url_for('main.reservations'))

@main_bp.route('/brewmaster-secret/reservations/remove/<int:reservation_id>', methods=['POST'])
def remove_reservation(reservation_id):
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    reservation = Reservation.query.get_or_404(reservation_id)

    try:
        db.session.delete(reservation)
        db.session.commit()
        flash('Бронь успешно удалена', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении брони: {str(e)}', 'error')

    return redirect(url_for('main.reservations'))


@main_bp.route('/brewmaster-secret/uploading/')
def uploading():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    if user.position_id == 2:
        return redirect(url_for('main.reservations'))

    

    return render_template('uploading.html')

@main_bp.route('/brewmaster-secret/uploading/get')
def get_reservations():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        flash('Неверный формат даты', 'danger')
        return redirect(url_for('main.uploading'))

    reservations = Reservation.query.filter(
        Reservation.date >= start_date,
        Reservation.date <= end_date
    ).order_by(Reservation.date, Reservation.start_time).all()

    data = []
    for r in reservations:
        admin_user = r.admin_user
        if admin_user:
            initials = f"{admin_user.last_name} {admin_user.first_name[0]}."
            if admin_user.middle_name:
                initials += f"{admin_user.middle_name[0]}."
        else:
            initials = '—'

        table_name = r.table.name if r.table else '—'
        status_name = r.status.name if r.status else '—'

        data.append({
            'ID': r.id,
            'Имя': r.name,
            'Телефон': r.phone,
            'Email': r.email,
            'Дата': r.date.strftime('%Y-%m-%d'),
            'Начало': r.start_time.strftime('%H:%M'),
            'Конец': r.end_time.strftime('%H:%M'),
            'Стол': table_name,
            'Статус': status_name,
            'Количество человек': r.num_people,
            'Особые пожелания': r.special_requests or '',
            'Создано': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Ответственный': initials,
        })


    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reservations')

    output.seek(0)

    filename = f"reservations_{start_date_str}_to_{end_date_str}.xlsx"

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@main_bp.route('/brewmaster-secret/staff/update/', methods=['POST'])
def update_user():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    if user.position_id == 2:
        return redirect(url_for('main.reservations'))

    user_id = request.form['user_id']
    user = AdminUser.query.get_or_404(user_id)

    user.last_name = request.form['last_name_edit']
    user.first_name = request.form['first_name_edit']
    user.middle_name = request.form['middle_name_edit']
    user.position_id = request.form['position_id_edit']

    db.session.commit()

    flash('Пользователь успешно обновлён', 'success')
    return redirect(url_for('main.admin_staff'))

@main_bp.route('/brewmaster-secret/staff/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    if user.position_id == 2:
        return redirect(url_for('main.reservations'))

    user_to_delete = AdminUser.query.get(user_id)

    if not user_to_delete:
        flash('Пользователь не найден', 'error')
        return redirect(url_for('main.admin_staff'))

    if user_id == admin_id:
        flash('Нельзя удалить свой аккаунт', 'error')
        return redirect(url_for('main.admin_staff'))

    db.session.delete(user_to_delete)
    db.session.commit()

    flash(f'Пользователь {user_to_delete.last_name} {user_to_delete.first_name[0]}. {user_to_delete.middle_name[0] if user_to_delete.middle_name else ""} успешно удален', 'success')

    return redirect(url_for('main.admin_staff'))

@main_bp.route('/brewmaster-secret/staff/add/', methods=['POST'])
def add_user():
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    if user.position_id == 2:
        return redirect(url_for('main.reservations'))

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    middle_name = request.form['middle_name']
    login = request.form['login']
    password = request.form['password']
    position_id = request.form['position_id']

    if AdminUser.query.filter_by(login=login).first():
        flash('Логин уже существует', 'error')
        return redirect(url_for('main.admin_staff'))
    new_user = AdminUser(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        login=login,
        position_id=position_id
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash('Пользователь успешно добавлен', 'success')
    return redirect(url_for('main.admin_staff'))


@main_bp.route('/brewmaster-secret/staff/edit/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    admin_id = session.get('admin_user_id')
    if not admin_id:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('auth.login'))

    user = AdminUser.query.get(admin_id)
    if not user:
        session.pop('admin_user_id', None)
        flash('Ваша учётная запись была удалена. Войдите снова.', 'warning')
        return redirect(url_for('auth.login'))

    if user.position_id == 2:
        return redirect(url_for('main.reservations'))

    user = AdminUser.query.get_or_404(user_id)
    if user:
            return jsonify({
                'id': user.id,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'login': user.login,
                'position_id': user.position.id,
            })
    return jsonify({'error': 'Пользователь не найден'}), 404

@main_bp.route('/reservations/get')
def user_reservations_get():
    date_str = request.args.get('date')
    time_start_str = request.args.get('time_start')
    time_end_str = request.args.get('time_end')
    people = int(request.args.get('people', 1))

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_start = datetime.strptime(time_start_str, '%H:%M').time()
        time_end = datetime.strptime(time_end_str, '%H:%M').time()
    except Exception as e:
        return jsonify({'error': 'Некорректные параметры'}), 400

    busy_reservations = Reservation.query.filter(
        Reservation.date == date,
        or_(
            and_(Reservation.start_time <= time_start, Reservation.end_time > time_start),
            and_(Reservation.start_time < time_end, Reservation.end_time >= time_end),
            and_(Reservation.start_time >= time_start, Reservation.end_time <= time_end)
        )
    ).all()

    busy_table_ids = {res.table_id for res in busy_reservations}

    available_tables = Table.query.filter(
        Table.capacity >= people,
        ~Table.id.in_(busy_table_ids)
    ).all()

    return jsonify([
        {'id': table.id, 'name': table.name, 'capacity': table.capacity}
        for table in available_tables
    ])

@main_bp.route('/table/<name>')
def get_table_by_name(name):
    table_name = name.replace('-', '.')
    table = Table.query.filter_by(name=table_name).first()
    if not table:
        return jsonify({'error': 'Стол не найден'}), 404

    return jsonify({
        'id': table.id,
        'name': table.name,
        'description': table.description,
        'photo': table.photo,
        'capacity': table.capacity,
        'deposit': table.deposit
    })

@main_bp.route('/api/time/now')
def get_nsk_time():
    tz = pytz.timezone('Asia/Novosibirsk')
    now = datetime.now(tz)
    return jsonify({
        'date': now.strftime('%Y-%m-%d'),
        'time': now.strftime('%H:%M')
    })

@main_bp.route('/reserve', methods=['POST'])
def create_reservation():
    data = request.get_json()

    try:
        table = Table.query.filter_by(name=data['table']).first()
        if not table:
            return jsonify({'error': 'Стол не найден'}), 404

        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['time_start'], '%H:%M').time()
        end_time = datetime.strptime(data['time_end'], '%H:%M').time()
        num_people = int(data['people'])

        new_reservation = Reservation(
            name=data['name'],
            status_id=1,
            date=date,
            start_time=start_time,
            end_time=end_time,
            table_id=table.id,
            num_people=num_people,
            phone=data['phone'],
            email=data.get('email'),
            special_requests=data.get('specialRequests')
        )

        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({'reservation_id': new_reservation.id}), 201

    except Exception as e:
        db.session.rollback()
        print('Ошибка при создании бронирования:', e)
        return jsonify({'error': 'Ошибка при создании бронирования'}), 500


@main_bp.route('/reservations/<int:reservation_id>')
def reservation_summary(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        abort(404, description="Бронирование не найдено")

    data = {
        'name': reservation.name,
        'table_name': reservation.table.name,
        'date': reservation.date.strftime('%d.%m.%Y'),
        'start_time': reservation.start_time.strftime('%H:%M'),
        'end_time': reservation.end_time.strftime('%H:%M'),
        'num_people': reservation.num_people
    }

    return render_template('reservation_thankyou.html', **data)


@main_bp.route('/')
def index():

    return render_template('index.html')
