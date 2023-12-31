from flask import Flask
from flask_login import login_user
from flask import request, session
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
# from datetime import datetime
# from datetime import datetime, timedelta
import datetime
import random
import json
from email.mime.text import MIMEText
import smtplib
import uuid
import re

app = Flask(__name__)
CORS(app)

client = MongoClient(
    'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority')
app.config['MONGO_URI'] = 'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = 'a6d217d048fdcd227661b755'
db = client['mcf_db']
# db2 = client['BnB_all_customers']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "ic2023wallet@gmail.com"
app.config['MAIL_PASSWORD'] = "irbnexpguzgxwdgx"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return 'home page'


# ------------------------------------------------------------------------------------------------------------

import requests
@app.route('/payment-requests', methods=['POST'])
def payment_request():
    try:
        # Receive data from frontend
        payment_data = request.get_json()
        order_data = payment_data['Odata']
        points = payment_data["points"]
        order_data['payment_status'] = 'pending'

        # Call the first API
        first_api_url = "https://api.sandbox.hit-pay.com/v1/payment-requests"
        first_api_payload = payment_data
        first_api_headers = {
            "X-BUSINESS-API-KEY": "dbabbd41e53aac95b5d6833e975fd2945f77e168450d70910d0248a0ccb83c1c",
            "Content-Type": "application/json"
        }

        first_api_response = requests.post(first_api_url, json=first_api_payload, headers=first_api_headers)
        first_api_data = first_api_response.json()

        # Get request id from the response
        request_id = first_api_data.get("id")
        order_data['oid'] = request_id

        # Call the second API with the received request id
        second_api_url = f"https://api.sandbox.hit-pay.com/v1/payment-requests/{request_id}"
        second_api_headers = {
            "X-BUSINESS-API-KEY": "dbabbd41e53aac95b5d6833e975fd2945f77e168450d70910d0248a0ccb83c1c"
        }

        second_api_response = requests.get(second_api_url, headers=second_api_headers)
        second_api_data = second_api_response.json()

        # Get the URL from the second API response
        url = second_api_data.get("url")
        order_data['payment_url'] = url

        # Return id and url
        return jsonify({"id": request_id, "url": url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/paymentStatus', methods=['GET'])
def get_payment_status():
    try:
        # Get request id from frontend
        request_id = request.args.get('request_id')

        # Call the payment status API
        payment_status_url = f"https://api.sandbox.hit-pay.com/v1/payment-requests/{request_id}"
        payment_status_headers = {
            "X-BUSINESS-API-KEY": "dbabbd41e53aac95b5d6833e975fd2945f77e168450d70910d0248a0ccb83c1c"
        }

        payment_status_response = requests.get(payment_status_url, headers=payment_status_headers)
        payment_status_data = payment_status_response.json()

        return jsonify({'id':request_id,'status':payment_status_data['status']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()





