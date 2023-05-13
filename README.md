# Chatbot Deployment with Flask and JavaScript

In this package I created a chatbot with Flask and JavaScript.

This app includes 13 endpoints and they are:
- `app.home`: renders the chatbot page
- `app.predict`: recieves message from the user and sends back an appropriate message
- `app.register`: registers a new admin
- `app.login`: logs in an admin
- `app.logout`: logs out an admin
- `app.admin`: renders the admin page
- `app.add`: adds a new item to the database
- `app.add_category`: adds a new category to the database
- `app.update`: updates an item in the database
- `app.update_category`: updates an category in the database
- `app.see_order`: renders a page that shows a particular order
- `app.fulfil`: an api endpoint for fulfilling orders
- `app.delete`: deletes an item or category

## Initial Setup:
This repo currently contains the starter files.

Clone repo and create a virtual environment
```
$ git clone https://github.com/python-engineer/chatbot-deployment.git
$ cd chatbot-deployment
$ python3 -m venv venv
$ . venv/bin/activate
```
Install dependencies
```
$ (venv) pip install Flask torch torchvision nltk
```
Install nltk package
```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```
Modify `intents.json` with different intents and responses for your Chatbot

Run
```
$ (venv) python train.py
```
This will dump data.pth file. And then run
the following command to test it in the console.
```
$ (venv) python chat.py
```
