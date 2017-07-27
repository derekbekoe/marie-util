import os
import logging
import requests
import time
import random
import string
import pymongo
import datetime

from flask import Flask, jsonify, request, render_template, redirect, make_response, session
from flask_cors import CORS, cross_origin


# This is random. You can make it whatever you want.
APP_SECRET_KEY = 'CEQvRYJXbXL7Wn2MzneRpgu445wbTm639fTLf9cBprHdbLUx'

# MongoDB connection string
MONGODB_URI = os.environ.get('MONGODB_URI')
# MongoDB database name
MONGODB_DB = 'mariestopes'
# MongoDB collection name
MONGODB_COLLECTION = 'locations'

def on_registration(form_data, user_id, user_given_name, user_family_name):
    attending = form_data.get('rsvp') == 'yes'
    transport_mode = form_data.get('transport-mode')
    sweatshirt_size = form_data.get('sweatshirt-size')
    restrictions = form_data.get('restrictions')
    client = pymongo.MongoClient(MONGODB_URI)
    reg_doc = {'user_id': user_id,
               'user_given_name': user_given_name,
               'user_family_name': user_family_name,
               'last_updated': datetime.datetime.now(),
               'attending': attending,
               'transport_mode': transport_mode,
               'sweatshirt_size': sweatshirt_size,
               'restrictions': restrictions}
    client[MONGODB_DB][MONGODB_COLLECTION].replace_one({'user_id': user_id}, reg_doc, upsert=True)
    return attending

def on_modify_location(form_data):
    county = form_data.get('county')
    region = form_data.get('region')
    facility = form_data.get('facility')
    location_desc = form_data.get('location_desc')
    client = pymongo.MongoClient(MONGODB_URI)
    reg_doc = {'county': county,
               'region': region,
               'facility': facility,
               'location_desc': location_desc}
    client[MONGODB_DB][MONGODB_COLLECTION].replace_one({'facility': facility}, reg_doc, upsert=True)

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = APP_SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if request.form.get('token') != APP_SECRET_KEY:
            return jsonify(ok=False), 400
        on_modify_location(request.form)
        return jsonify(ok=True)

if __name__ == "__main__":
    app.run()
