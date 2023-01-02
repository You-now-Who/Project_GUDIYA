from os import path
from flask import Flask, render_template, request, jsonify, redirect, make_response
from make_predictions import get_final_output
print("Imported Final Output")
from responses import conv_res
print("Imported responses Output")
# from run_chatbot import chatbot_response, woman_in_stem_response, fav_subject_response, your_career_response
# import speech_recognition as sr
from translate_req import translate_request
from run_chatbot import chatbot_response, woman_in_stem_response, fav_subject_response, your_career_response
print("Imported translate")
import os
# # from config import SECRET_KEY
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from dotenv import load_dotenv
# import os
# from flask_restful import Resource, Api

# try:
#     from config import SECRET_KEY, DB_URI_REAL
#     DATABASE_URL = DB_URI_REAL

# except:
#     SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(12).hex())
#     DATABASE_URL = os.getenv('DB_URI_REAL', os.urandom(12).hex())

# db = SQLAlchemy()
# DB_NAME = "database.db"

# from gtts import gTTS

languages_list = {"Afrikaans": "af",
"Albanian": "sq",
"Amharic": "am",
"Arabic": "ar",
"Armenian": "hy",
"Assamese": "as",
"Azerbaijani (Latin)": "az",
"Bangla": "bn",
"Bashkir": "ba",
"Basque": "eu",
"Bosnian (Latin)": "bs",
"Bulgarian": "bg",
"Cantonese (Traditional)": "yue",
"Catalan": "ca",
"Chinese (Literary)": "lzh",
"Chinese Simplified": "zh-Hans",
"Chinese Traditional": "zh-Hant",
"Croatian": "hr",
"Czech": "cs",
"Danish": "da",
"Dari": "prs",
"Divehi": "dv",
"Dutch": "nl",
"English": "en",
"Estonian": "et",
"Faroese": "fo",
"Fijian": "fj",
"Filipino": "fil",
"Finnish": "fi",
"French": "fr",
"French (Canada)": "fr-ca",
"Galician": "gl",
"Georgian": "ka",
"German": "de",
"Greek": "el",
"Gujarati": "gu",
"Haitian Creole": "ht",
"Hebrew": "he",
"Hindi": "hi",
"Hmong Daw (Latin)": "mww",
"Hungarian": "hu",
"Icelandic": "is",
"Indonesian": "id",
"Inuinnaqtun": "ikt",
"Inuktitut": "iu",
"Inuktitut (Latin)": "iu-Latn",
"Irish": "ga",
"Italian": "it",
"Japanese": "ja",
"Kannada": "kn",
"Kazakh": "kk",
"Khmer": "km",
"Klingon": "tlh-Latn",
"Klingon (plqaD)": "tlh-Piqd",
"Korean": "ko",
"Kurdish (Central)": "ku",
"Kurdish (Northern)": "kmr",
"Kyrgyz (Cyrillic)": "ky",
"Lao": "lo",
"Latvian": "lv",
"Lithuanian": "lt",
"Macedonian": "mk",
"Malagasy": "mg",
"Malay (Latin)": "ms",
"Malayalam": "ml",
"Maltese": "mt",
"Maori": "mi",
"Marathi": "mr",
"Mongolian (Cyrillic)": "mn-Cyrl",
"Mongolian (Traditional)": "mn-Mong",
"Myanmar": "my",
"Nepali": "ne",
"Norwegian": "nb",
"Odia": "or",
"Pashto": "ps",
"Persian": "fa",
"Polish": "pl",
"Portuguese (Brazil)": "pt",
"Portuguese (Portugal)": "pt-pt",
"Punjabi": "pa",
"Queretaro Otomi": "otq",
"Romanian": "ro",
"Russian": "ru",
"Samoan (Latin)": "sm",
"Serbian (Cyrillic)": "sr-Cyrl",
"Serbian (Latin)": "sr-Latn",
"Slovak": "sk",
"Slovenian": "sl",
"Somali (Arabic)": "so",
"Spanish": "es",
"Swahili (Latin)": "sw",
"Swedish": "sv",
"Tahitian": "ty",
"Tamil": "ta",
"Tatar (Latin)": "tt",
"Telugu": "te",
"Thai": "th",
"Tibetan": "bo",
"Tigrinya": "ti",
"Tongan": "to",
"Turkish": "tr",
"Turkmen (Latin)": "tk",
"Ukrainian": "uk",
"Upper Sorbian": "hsb",
"Urdu": "ur",
"Uyghur (Arabic)": "ug",
"Uzbek (Latin": "uz",
"Vietnamese": "vi",
"Welsh": "cy",
"Yucatec Maya": "yua",
"Zulu": "zu"}



global curr_lang
curr_lang = 'English'


# def woman_in_stem_response():
#     return("lol woman response")

# def fav_subject_response():
#     return("lol subject response")

# def your_career_response():
#     return("lol career response")

global code
code = "NONE"
level = 0
dic_first_code_response = {
    "CODE_WOMAN_IN_STEM": ["Would you like to hear about a famous woman in STEM?", woman_in_stem_response],
    "CODE_CHANGE_LANG": ["What language do you want to change to?", woman_in_stem_response],
    "CODE_FAV_SUBJECT": ["What is your favourite subject?", fav_subject_response],
    "CODE_CAREER_GUIDANCE": ["What do you want to be when you grow up?", your_career_response]
                            }

languages = {
    'marathi': 'mr',
    'hindi': 'hi',
    'english': 'en'
}

recognize_lang = {
        'marathi': 'mr-IN',
        'hindi': 'hi-IN',
        'english': 'en-US'
    }

# translator_human = Translator('hi', 'en')
# translator_bot = Translator('en', 'hi')


app = Flask(__name__)

# app.secret_key = SECRET_KEY
# # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# db.init_app(app)

# api = Api(app)
# from auth import auth
# from models import User, Inputs

# app.register_blueprint(auth, url_prefix="/")

# if not path.exists(DB_NAME):
#     with app.app_context():
#         db.create_all()
#     print('\n\nCreated Database!\n\n')

# # create_database(app)
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))

print("Import Complete")

@app.route("/")
def home():
    return render_template("index.html", user="current_user")

@app.route("/text")
def text():
    return render_template("text.html", user="current_user")

@app.route("/virtual_doll")
def doll():
    return render_template("virtual_doll.html", user="current_user")

# @app.route("/login")
# def login():
#     return render_template("login.html")

# @app.route("/signup")
# def signup():
#     return render_template("signup.html")
# def create_database(app):


@app.route("/get")
def get_bot_response():
    global code, level
    userText = request.args.get('msg')
    # activeCode = request.args.get('currentCode')
    
    if userText == "":
        return "Please type something"
    
    try:
        new_msg = Inputs(msg=userText, code=code, user_id=current_user.id)
        db.session.add(new_msg)
        db.session.commit()
        print('Message added to database: ', userText)
    except:
        pass
    

    if code == "NONE":
        res = chatbot_response(userText)

        print("Crossing you")
        print(res)
        print("\n\n\n")

        try:
            if res[:4] == "CODE":
                code = res
                level = level + 1
                
                print(dic_first_code_response[code][0])
                return make_response(translate_request(dic_first_code_response[code][0], languages_list[curr_lang])["translated_text"])
                # return dic_first_code_response[code][0]
            
            elif res == "CONVERSATION":
                return make_response(translate_request(conv_res(userText), languages_list[curr_lang])["translated_text"])

            else:
                print(curr_lang)
                # print(languages_list[curr_lang])
                print(translate_request(res, languages_list[curr_lang])["translated_text"])
                return make_response(translate_request(res, languages_list[curr_lang])["translated_text"])


        except Exception as e:
            print(e)
            return("Internal Error Occured")

    
    else:
        print("Reached code: ", code)
        level += 1
        res, level = dic_first_code_response[code][1](userText, level)
        print("Response code: ", res)
        if level == 0:
            code = "NONE"
        print("This is the response: ", res)
        return make_response(translate_request(res, languages_list[curr_lang])["translated_text"])
    


@app.route("/getcode")
def get_code_response():
    global code
    return jsonify({
        "code": code,
        "level": level
    })


@app.route("/changelanguage")
def change_language():
    global curr_lang
    print(curr_lang)
    curr_lang = request.args.get('language')
    print(curr_lang)
    return make_response("res")




if __name__ == "__main__":

    # app.secret_key = SECRET_KEY
    # translator_human = Translator('hi', 'en')
    # translator_bot = Translator('en', 'hi')
    # dotenv_path = '.env'  # Path to .env file
    # load_dotenv(dotenv_path)

    app.run(debug=True)