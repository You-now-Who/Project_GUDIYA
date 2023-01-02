from sub_py.responses import conv_res, stem_res
import os
#import shutil
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import seaborn as sns
import tensorflow_text as text
import numpy as np

from os import path
from flask import Flask, render_template, request, jsonify, redirect, make_response
import speech_recognition as sr
from translate import Translator
# from config import SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os

try:
    from config import SECRET_KEY, DB_URI_REAL
    DATABASE_URL = DB_URI_REAL

except:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(12).hex())
    DATABASE_URL = "postgresql://etgkockybkxera:bb47a81ba8bdf330a2df8dfe6243486042b78728c626f852cfd4f832e67da889@ec2-52-23-131-232.compute-1.amazonaws.com:5432/desv0hpo0570hd"

db = SQLAlchemy()
DB_NAME = "database.db"

def do_nothing():
    pass

dic_first_code_response = {
    "CODE_WOMAN_IN_STEM": ["Would you like to hear about a famous woman in STEM?", do_nothing],
    "CODE_CHANGE_LANG": ["What language do you want to change to?", do_nothing],
    "CODE_FAV_SUBJECT": ["What is your favourite subject?", do_nothing],
    "CODE_CAREER_GUIDANCE": ["What do you want to be when you grow up?", do_nothing]
                            }

# from gtts import gTTS

# translator_bot = Translator(from_lang = "en", to_lang="mr")
# translator_human = Translator(from_lang = "mr", to_lang="en")


# from sub_py.responses import conv_res, stem_res

import matplotlib.pyplot as plt
tf.get_logger().setLevel('ERROR')


import warnings
warnings.filterwarnings("ignore")

classes = ['GREETING', 'CONVERSATION', 'STEM']
new_model = tf.keras.models.load_model('my_model.h5', custom_objects={'KerasLayer':hub.KerasLayer})

def predict_class(user_input):
    predictions = new_model.predict([user_input])
    pred_class = classes[np.argmax(predictions)]
    return(pred_class)

# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large", padding_side='right')
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

app = Flask(__name__)

app.secret_key = SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

from sub_py.models import User, Inputs
from sub_py.auth import auth

app.register_blueprint(auth, url_prefix="/")

if not path.exists(DB_NAME):
    with app.app_context():
        db.create_all()
    print('\n\nCreated Database!\n\n')

# create_database(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
def home():
    return render_template("index.html", user=current_user)

@app.route("/text")
def text():
    return render_template("text.html", user=current_user)

@app.route("/virtual_doll")
def doll():
    return render_template("virtual_doll.html", user=current_user)

@app.route("/get")
def get_bot_response():
    global code, level
    userText = request.args.get('msg')
    # activeCode = request.args.get('currentCode')
    
    if userText == "":
        return "Please type something"
    
    try:
        return "RESPONSE"
    except:
        return "Sorry, I didn't understand that"
    


@app.route("/getcode")
def get_code_response():
    global code
    return jsonify({
        "code": code,
        "level": level
    })



@app.route("/audio",  methods=["GET", "POST"])
def audio():
    # transcript = ""
    if request.method == "POST":
        pass
    else:
        return render_template("audio.html", user=current_user)


@app.route("/get_audio", methods=["GET", "POST"])
def get_audio():
    if request.method == "POST":

        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        r = sr.Recognizer()
        with sr.AudioFile("audio.wav") as source:
            audio = r.record(source)
            try:
                s = r.recognize_google(audio)
                print("Text: "+s)
                return s
            except Exception as e:
                print("Exception: "+str(e))
                return "*unintelligible*"

            # except Exception as e:
            #     print("Sorry, I did not get that  ", e)
            #     return "Sorry, I did not get that"
    else:
        return render_template("audio.html")



if __name__ == "__main__":

    # app.secret_key = SECRET_KEY
    translator_human = Translator('hi', 'en')
    translator_bot = Translator('en', 'hi')
    dotenv_path = '.env'  # Path to .env file
    load_dotenv(dotenv_path)

    app.run(debug=True)