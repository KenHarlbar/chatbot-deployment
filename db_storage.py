from flask_login import UserMixin
from pony.orm import *
from datetime import datetime

db = Database()


class User(db.Entity, UserMixin):
    _table_: 'users'
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    password = Required(str)
    items = Set('Item')
    categories = Set('Category')


class Item(db.Entity):
    _table_: 'items'
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    price = Required(int)
    description = Optional(str)
    category = Required('Category')
    order_items = Set('OrderItem')
    added_by = Required('User')
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)


class OrderItem(db.Entity):
    _table_ = 'order_items'
    id = PrimaryKey(int, auto=True)
    order = Required('Order')
    item = Required('Item')
    quantity = Required(int, default=1)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)


class Order(db.Entity):
    _table_: 'orders'
    id = PrimaryKey(int, auto=True)
    order_items = Set('OrderItem')
    fulfilled = Required(bool, default=False)
    name_of_buyer = Required(str)
    phone_number = Required(str)
    address = Required(str)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)


class Category(db.Entity):
    _table_: 'categories'
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    items = Set('Item')
    added_by = Required('User')
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)


db.bind(provider="sqlite", filename="chatbot.db", create_db=True)
db.generate_mapping(create_tables=True)
