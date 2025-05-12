# ─────────────────────────────────────────────────────────────────────────────
# СХЕМА СВЯЗЕЙ МЕЖДУ МОДЕЛЯМИ (ОТНОШЕНИЯ "ОДИН-КО-МНОГИМ"):
#
# Position (1) ⇨ (∞) AdminUser
#   • Один объект Position (должность) может быть у нескольких пользователей.
#   • Поле: AdminUser.position_id → positions.id
#
# AdminUser (1) ⇨ (∞) Reservation
#   • Один админ может создать множество бронирований (опционально).
#   • Поле: Reservation.admin_user_id → admin_users.id
#
# Status (1) ⇨ (∞) Reservation
#   • Один статус используется в нескольких бронированиях.
#   • Поле: Reservation.status_id → statuses.id
#
# Table (1) ⇨ (∞) Reservation
#   • Один стол может быть забронирован много раз.
#   • Поле: Reservation.table_id → tables.id
# ─────────────────────────────────────────────────────────────────────────────

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship

class Table(db.Model):
    # Модель стола: имя, описание, фото, вместимость, депозит
    # Используется в бронированиях (связь один-ко-многим)
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=1)
    deposit = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<Table {self.name}>'

class Position(db.Model):
    # Должности администраторов (например, "Администратор", "Хостес")
    # Связана с AdminUser через position_id
    __tablename__ = 'positions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    users = db.relationship('AdminUser', backref='position', lazy=True)

    def __repr__(self):
        return f'<Position {self.name}>'

class AdminUser(db.Model):
    # Администратор системы: ФИО, логин, пароль, должность
    # Может быть автором бронирований (admin_user_id в Reservation)
    # Использует методы set_password и check_password для хеширования
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.login}>'

class Status(db.Model):
    # Статусы бронирования
    # Связан с Reservation через status_id
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    reservations = db.relationship('Reservation', backref='status', lazy=True)

class Reservation(db.Model):
    # Бронирование: имя клиента, статус, дата и время, стол, количество гостей, контакты, примечания
    # Может быть создано администратором (admin_user_id), связано с Table и Status
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    special_requests = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_user_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=True)
    
    admin_user = relationship('AdminUser', backref='reservations')
    table = relationship('Table', backref='reservations')

    def __init__(self, name, status_id, date, start_time, end_time, table_id, num_people, phone, email=None, special_requests=None, admin_user_id=None):
        self.name = name
        self.status_id = status_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.table_id = table_id
        self.num_people = num_people
        self.phone = phone
        self.email = email
        self.special_requests = special_requests
        self.admin_user_id = admin_user_id


    def __repr__(self):
        return f"<Reservation {self.name} on {self.date} from {self.start_time} to {self.end_time}>"