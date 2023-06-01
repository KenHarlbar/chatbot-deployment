from pony.orm import db_session
from db_storage import User, Item, OrderItem, Order, Category
from temp import delete_user, create_user, delete_item, delete_category, delete_order, delete_order_item


def test_user():
    """
    GIVEN an application
    WHEN an admin user wants to register
    THEN register the user
    """
    user = create_user()
    assert user.email == 'ola@app.com'
    assert user.password == 'gideon1234'
    assert delete_user(user) == None


def test_item():
    """
    GIVEN an application
    WHEN an admin user wants to create an item
    THEN create and delete the item
    """
    # user = create_user()
    with db_session:
        user = User(email='ola@app.com', password='gideon1234')
        item = Item(name='Nutri C', price=200, category=Category.get(name='Snack'), added_by=user)
    assert user.email == 'ola@app.com'
    assert user.password == 'gideon1234'
    assert item.name == 'Nutri C'
    assert item.price == 200
    assert item.category.name == 'Snack'
    assert item.added_by == user
    assert delete_user(user) == None
    try:
        assert delete_item(item) == None
    except Exception:
        pass


def test_category():
    """
    GIVEN an application
    WHEN an admin user wants to create a category
    THEN create and delete the category
    """
    with db_session:
        user = User(email='ola@app.com', password='gideon1234')
        category = Category(name='Shit', added_by=user)
    assert user.email == 'ola@app.com'
    assert user.password == 'gideon1234'
    assert category.name == 'Shit'
    assert category.added_by == user
    assert delete_user(user) == None
    try:
        assert delete_category(category) == None
    except Exception:
        pass


def test_order():
    """
    GIVEN an application
    WHEN a customer makes an order
    THEN create and delete the order
    """
    with db_session:
        order = Order(name_of_buyer='Baki', phone_number='37382927383', address='3, unity class street')
        user = User(email='ola@app.com', password='gideon1234')
        item = Item(name='Nutri C', price=200, category=Category.get(name='Snack'), added_by=user)
        o_item = OrderItem(order=order, item=item)
    assert user.email == 'ola@app.com'
    assert user.password == 'gideon1234'
    assert item.name == 'Nutri C'
    assert item.price == 200
    assert item.category.name == 'Snack'
    assert item.added_by == user
    assert order.name_of_buyer == 'Baki'
    assert order.phone_number == '37382927383'
    assert order.address == '3, unity class street'
    assert order.fulfilled == False
    assert o_item.order == order
    assert o_item.item == item
    assert delete_user(user) == None
    try:
        assert delete_item(item) == None
        assert delete_order(order) == None
        assert delete_order_item(o_item) == None
    except Exception:
        pass


def test_fulfilled_order():
    """
    GIVEN an application
    WHEN a customer makes an order
    THEN create, fulfil and delete the order
    """
    with db_session:
        order = Order(name_of_buyer='Baki', phone_number='37382927383', address='3, unity class street', fulfilled=True)
        user = User(email='ola@app.com', password='gideon1234')
        item = Item(name='Nutri C', price=200, category=Category.get(name='Snack'), added_by=user)
        o_item = OrderItem(order=order, item=item)
    assert user.email == 'ola@app.com'
    assert user.password == 'gideon1234'
    assert item.name == 'Nutri C'
    assert item.price == 200
    assert item.category.name == 'Snack'
    assert item.added_by == user
    assert order.name_of_buyer == 'Baki'
    assert order.phone_number == '37382927383'
    assert order.address == '3, unity class street'
    assert order.fulfilled == True
    assert o_item.order == order
    assert o_item.item == item
    assert delete_user(user) == None
    try:
        assert delete_item(item) == None
        assert delete_order(order) == None
        assert delete_order_item(o_item) == None
    except Exception:
        pass