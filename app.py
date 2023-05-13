from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from pony.orm import *
from chat import get_response
from db_storage import Item, Category, Order, User, OrderItem
from forms import RegisterForm, LoginForm, PostForm, PostCategoryForm
from config import Config
from utils import (
    prompt,
    add_prompt,
    add_another_prompt,
    order_prompt,
    top_categories,
    categories,
    ask_name,
    ask_address,
    ask_phone_number,
    confirmation,
    confirm,
)


app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
bcrypt = Bcrypt()
bcrypt.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    with db_session:
        return User.get(id=int(user_id))


@app.get("/")
def home():
    """Render the home page"""
    return render_template("base.html")


@app.post("/predict")
def predict():
    """Process the input and give an output"""
    response = ""
    text = request.get_json().get("message")
    orders = request.get_json().get("orders", [])
    prev_msg = request.get_json().get("prevMsg")
    prev_2_msg = request.get_json().get("prev2Msg")
    # Level 1
    if prev_msg == order_prompt:
        try:
            response = prompt(top_categories[int(text) - 1])
        except Exception as e:
            pass
    # Level 2
    for category in top_categories:
        if prev_msg == prompt(category):
            try:
                with db_session:
                    item = Item[int(text)]
                if item != None:
                    orders.append(item.id)
                    response = add_prompt()
            except Exception as e:
                pass
    # Level 3
    if prev_msg == add_prompt():
        try:
            with db_session:
                response = prompt(Category[int(text)].name)
        except Exception as e:
            print(e)
    # Level 4
    for category in categories():
        if prev_msg == prompt(category.name) and prev_2_msg == add_prompt():
            try:
                with db_session:
                    item = Item[int(text)]
            except Exception as e:
                print(e)
            if item != None:
                orders.append(item.id)
                response = add_another_prompt
    # Level 5
    if prev_msg == add_another_prompt:
        if text == "1":
            response = add_prompt()
        else:
            response = ask_name
    if prev_msg == ask_name:
        orders.append(text)
        response = ask_address
    if prev_msg == ask_address:
        orders.append(text)
        response = ask_phone_number
    if prev_msg == ask_phone_number:
        orders.append(text)
        response = confirm(orders)
    if prev_msg == confirm(orders):
        if text.lower() == "confirm":
            with db_session:
                order = Order(
                    name_of_buyer=orders[-3],
                    address=orders[-2],
                    phone_number=orders[-1],
                )
                print(order)
                for i in range(len(orders) - 3):
                    order.order_items.create(item=Item[int(orders[i])])
                    print(order.order_items)
            response = confirmation
        else:
            orders = []
            response = order_prompt
    if response == confirmation:
        orders = []
    # if the above "if" statements doesn't fit
    if response == "":
        response = get_response(text)
    if response == "I do not understand...":
        orders = []
    message = {"answer": response, "orders": orders}
    return jsonify(message)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        with db_session:
            user = User(
                password=hashed_password,
                email=form.email.data,
            )
        flash(
            "Your account has been created, \
                you are now able to log in",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin"))
    form = LoginForm()
    if form.validate_on_submit():
        with db_session:
            user = User.get(email=form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("admin"))
        else:
            flash(
                "Login Unsuccessful, please check \
                    username and password",
                "danger",
            )
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """Admin route for making crud operations"""
    with db_session:
        items = Item.select().order_by(Item.updated_at)[:]
        orders = Order.select()[:]
        categories = Category.select().order_by(desc(Category.updated_at))[:]
        return render_template(
            "admin.html",
            title="Admin",
            items=items,
            orders=orders,
            categories=categories,
        )


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Route to add menu"""
    form = PostForm(meta={"csrf": False})
    if form.validate_on_submit():
        with db_session:
            item = Item(
                name=form.name.data.strip().capitalize(),
                price=form.price.data,
                description=form.description.data.strip().capitalize(),
                category=Category.get(name=form.category.data.strip().capitalize()).id,
                added_by=current_user.id,
            )
        flash(Item.__name__ + " Added Successfully!", "success")
        return redirect(url_for("admin"))
    return render_template("add.html", form=form, title="Add " + Item.__name__)


@app.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
    """Route to add category"""
    form = PostCategoryForm(meta={"csrf": False})
    if form.validate_on_submit():
        with db_session:
            item = Category(
                name=form.name.data.strip().capitalize(), added_by=current_user.id
            )
        flash(Category.__name__ + " Added Successfully!", "success")
        return redirect(url_for("admin"))
    return render_template("add_category.html", form=form, title="Add " + Item.__name__)


@app.route("/update/<int:item_id>", methods=["GET", "POST"])
@login_required
def update(item_id):
    with db_session:
        item = Item[item_id]
    form = PostForm()
    if form.validate_on_submit():
        with db_session:
            item = Item[item_id]
            item.name = form.name.data.strip().capitalize()
            item.price = form.price.data
            item.category = Category.get(name=form.category.data.strip()).capitalize()
            item.description = form.description.data.strip().capitalize()
        flash("Your item has been updated!", "success")
        return redirect(url_for("admin"))
    form.name.data = item.name
    form.price.data = item.price
    with db_session:
        form.category.data = Category[str(item.category)[-2]].name
    form.description.data = item.description
    return render_template(
        "add.html", title="Update Item", form=form, legend="Update Item"
    )


@app.route("/update_category/<int:item_id>", methods=["GET", "POST"])
@login_required
def update_category(item_id):
    with db_session:
        item = Category[item_id]
    form = PostCategoryForm()
    if form.validate_on_submit():
        with db_session:
            item = Category[item_id]
            item.name = form.name.data.strip().capitalize()
        flash("Your item has been updated!", "success")
        return redirect(url_for("admin"))
    form.name.data = item.name
    return render_template(
        "add_category.html", title="Update Item", form=form, legend="Update Item"
    )


@app.route("/see_order/<int:order_id>", methods=["GET", "POST"])
@login_required
def see_order(order_id):
    with db_session:
        order = Order[order_id]
        order_items = OrderItem.select()[:]
    new_order_items = []
    order_items_items = []
    items = []
    total_cost = 0
    for order_item in order_items:
        if order_item.order == order:
            new_order_items.append(order_item)
    for order_item in new_order_items:
        order_items_items.append(order_item.item)
    for item in order_items_items:
        id = int(str(item)[5:-1])
        with db_session:
            items.append(Item.get(id=id))
    for item in items:
        total_cost += item.price
    combined = zip(items, new_order_items)
    print(new_order_items)
    print(order_items_items)
    return render_template(
        "see_order.html",
        title="See Order",
        order=order,
        order_items=new_order_items,
        items=items,
        total=total_cost,
        combined=combined,
    )


@app.route("/fulfil/<int:order_id>", methods=["GET", "POST"])
@login_required
def fulfil(order_id):
    with db_session:
        order = Order[order_id]
        order.fulfilled = True
    return redirect(url_for("admin"))


@app.route("/delete/<string:entity>/<int:item_id>", methods=["GET", "POST"])
@login_required
def delete(entity, item_id):
    with db_session:
        item = eval(entity)[item_id]
    if item:
        with db_session:
            eval(entity)[item_id].delete()
        flash("Your item has been deleted!", "success")
        return redirect(url_for("admin"))
    flash("Something is wrong!")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True, port=3000)
