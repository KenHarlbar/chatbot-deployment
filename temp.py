from pony.orm import db_session
from db_storage import User, Item, Category, Order, OrderItem


def delete_user(obj):
    with db_session:
        User[obj.id].delete()
        return User.get(id=obj.id)
    

def create_user():
    with db_session:
        user = User(email='ola@app.com', password='gideon1234')
    return user


def delete_item(item):
    with db_session:
        Item[item.id].delete()
        return None
    

def delete_category(category):
    with db_session:
        Category[category.id].delete()
        return None
    

def delete_order(order):
    with db_session:
        Order[order.id].delete()
        return None
    

def delete_order_item(o_item):
    with db_session:
        OrderItem[o_item.id].delete()
        return None
    
# print(delete_user())

if __name__ == '__main__':
    with db_session:
        user = User.get(email='ola@app.com')
        User[user.id].delete()
        print(User.get(id=user.id))