import json as js
from pony.orm import db_session
import requests
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
from db_storage import Category


def test_predict():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a get request is sent to the '/predict' endpoint
    THEN check that the returned status code is 405
    """
    response = requests.get('http://localhost:3000/predict')
    assert response.status_code == 405


def test_greeting():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to the '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': 'Hi'})
    assert response.status_code == 200
    assert 'Hi' in response.text or 'Hello' in response.text


def test_goodbye():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': 'Bye'})
    assert response.status_code == 200
    assert 'See' in response.text or 'Have' in response.text or 'Bye' in response.text


def test_items():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': 'Which foods do you have?'})
    assert response.status_code == 200
    assert 'Traditional' in response.text or 'Snacks' in response.text or 'Drinks' in response.text


def test_order():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': 'Yes, I want to place an order now'})
    assert response.status_code == 200
    assert 'Great' in response.text or 'Category' in response.text or '\n' in response.text

def test_level_1():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': '1', 'prevMsg': order_prompt})
    assert response.status_code == 200
    assert prompt(top_categories[0]) == js.loads(response.text)['answer']


def test_level_2():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': '4', 'prevMsg': prompt(top_categories[0])})
    assert response.status_code == 200
    assert add_prompt() == js.loads(response.text)['answer']


def test_level_3():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': '8', 'prevMsg': add_prompt()})
    assert response.status_code == 200
    with db_session:
        assert prompt(Category[8].name) == js.loads(response.text)['answer']


def test_level_4():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    with db_session:
        response = requests.post('http://localhost:3000/predict', json={'message': '5', 'prevMsg': prompt(Category[8].name), 'prev2Msg': add_prompt()})
    assert response.status_code == 200
    assert add_another_prompt == js.loads(response.text)['answer']


def test_level_5():
    """
    GIVEN a flask endpoint configured for testing
    WHEN a post request is sent to '/predict' endpoint
    THEN check that the returned text is correct
    """
    response = requests.post('http://localhost:3000/predict', json={'message': '1', 'prevMsg': add_another_prompt})
    assert response.status_code == 200
    assert add_prompt() == js.loads(response.text)['answer']