from db_storage import Item, Category
from pony.orm import *


def prompt(var) -> str:
    """Ret"""
    prompt: str = ""
    with db_session:
        items = Item.select()[:]
    for item in items:
        with db_session:
            name = Category[str(item.category)[-2]].name
        if name == var.capitalize():
            string: str = ""
            string += "{}. {} @{}".format(item.id, item.name, item.price)
            if item != items[-1]:
                string += "\n"
            prompt += string
    return prompt


def add_prompt() -> str:
    """Ret"""
    prompt: str = "Which of the following do you still want to add?\n"
    with db_session:
        categories = Category.select()[:]
    new_categories = []
    for category in categories:
        if category.name not in top_categories and category not in new_categories:
            new_categories.append(category)
    for category in new_categories:
        string: str = ""
        string += "{}. {}".format(category.id, category.name)
        if category != new_categories[-1]:
            string += "\n"
        prompt += string
    return prompt


def categories() -> list:
    with db_session:
        categories = Category.select()[:]
    for category in categories:
        if category in top_categories:
            categories.remove(category)
    return categories


def confirm(orders) -> str:
    response = 'Please confirm your order by typing "confirm":\n'
    total_cost = 0
    for i in range(len(orders) - 3):
        string = ""
        with db_session:
            item = Item[int(orders[i])]
        total_cost += item.price
        string += "{}. {}\n".format(i + 1, item.name)
        response += string
    # response += "\nName: {}\nAddress: {}\nPhone Number: {}".format(
    #     orders[len(orders) - 3], orders[len(orders) - 2], orders[len(orders) - 1]
    # )
    response += "\n\n Total is {}".format(total_cost)
    return response


top_categories = ["Snack", "Dish"]
add_another_prompt: str = "Do you want to add another?\n1. Yes\n2. No"
order_prompt: str = "Great! Pick a category of food to order\n\t1. Snacks and Drinks\n\t2. Traditional dish"
ask_name: str = "What is your name?"
ask_address: str = "What is your address"
ask_phone_number: str = "Enter your phone number"
confirmation: str = "Congratulations! your order has been booked, Our rider will get to you shortly.\nThank you for patronizing us."
