import re
# import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer
# nltk.download()
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
# from keras.models import load_model
from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5', compile=False)
import json
import random
# import pyaudio

# from translate import Translator

# translator_bot = Translator(from_lang = "en", to_lang="mr")
# translator_human = Translator(from_lang = "mr", to_lang="en")

# import pyttsx3

from huggingface_hub import list_models

# from transformers import MarianMTModel, MarianTokenizer
from typing import Sequence

# class Translator:
#     def __init__(self, source_lang: str, dest_lang: str) -> None:
#         self.model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{dest_lang}'
#         self.model = MarianMTModel.from_pretrained(self.model_name)
#         self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        
#     def translate(self, texts: Sequence[str]) -> Sequence[str]:
#         tokens = self.tokenizer(list(texts), return_tensors="pt", padding=True)
#         translate_tokens = self.model.generate(**tokens)
#         return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translate_tokens]
        
# global translator_human
# global translator_bot

# translator_human = Translator('hi', 'en')
# translator_bot = Translator('en', 'hi')

global curr_lang
curr_lang = 'english'



# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(info['index'], info['name'])

# engine = pyttsx3.init()

# voices = engine.getProperty('voices')
# for voice in voices:
#     print(f"Voice: {voice.name}")
# engine.setProperty('voice', voices[1].id)

# #""" RATE"""
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
# engine.setProperty('rate', 175)     # setting up new voice rate

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

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


# RETURN WOMAN IN STEM ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def woman_in_stem_response():

#     bot_output("Would you like to hear about a famous woman?")

#     while True:


#         women_list = [
#             "Katherine Johnson was a NASA space scientist. Born in ninteen eighteen, she graduated from university at the age of 18. She was awarded the prestigious Presidential Medal of freedom in two thousand fifteen for her contirbutions to physics and mathematics.",
#             "Radia Perlman an early computer scientist and student of MIT. She was a pioneer of the internet. She developed the algorithm behind the Spanning Tree Protocol (STP), an innovation that made today’s Internet possible. She also invented TRILL to correct limitations of STP as well.",
#             "Dr. Priya Abraham, an alumna of Christian Medical College in Vellore, India and the former head of the department of Clinic Virology, was appointed in November 2019 as the Director of the National Institute of Virology (NIV) in Pune, India—not knowing she would be confronted with a global pandemic merely two months later. With her team at NIV, Dr. Priya Abraham has been instrumental in isolating and sequencing strains of the SARS-CoV-2, the virus responsible for the COVID-19 pandemic."
            
#         ]

#         user_input = mic_input()

#         check_sentiment = get_secondary_response(user_input, "YES/NO")

#         if check_sentiment == "YES":
#             bot_output("\nOk, here is a leading woman in STEM: \n")
#             return random.choice(women_list)
#             break
        
#         elif check_sentiment == "NO":
#             return "No problem!"
#             break

#         else:
#             bot_output("I am sorry, I could not understand that. Was that a yes or a no?")
        

def woman_in_stem_response(input, level):

    women_list = [
            "Katherine Johnson was a NASA space scientist. Born in ninteen eighteen, she graduated from university at the age of 18. She was awarded the prestigious Presidential Medal of freedom in two thousand fifteen for her contirbutions to physics and mathematics.",
            "Radia Perlman was an early computer scientist and student of MIT. She was a pioneer of the internet. She developed the algorithm behind the Spanning Tree Protocol (STP), an innovation that made today’s Internet possible. She also invented TRILL to correct limitations of STP as well.",
            "Dr. Priya Abraham, an alumna of Christian Medical College in Vellore, India and the former head of the department of Clinic Virology, was appointed in November 2019 as the Director of the National Institute of Virology (NIV) in Pune, India—not knowing she would be confronted with a global pandemic merely two months later. With her team at NIV, Dr. Priya Abraham has been instrumental in isolating and sequencing strains of the SARS-CoV-2, the virus responsible for the COVID-19 pandemic."
            
        ]
    print("Reached the WOMAN IN STEM RESPONSE\n")
    # if level == 1:
    #     return("Would you like to hear about a famous woman?", 2)
    # bot_output("Would you like to hear about a famous woman?")

    if level == 2:
        check_sentiment = get_secondary_response(input, "YES/NO")

        if check_sentiment == "YES":
            return (random.choice(women_list), 0)

        elif check_sentiment == "NO":
            return ("No problem!", 0)

        else:
            return("I am sorry, I could not understand that. Was that a yes or a no?", 1)


def your_career_response(input, level):
    
        print("Reached the YOUR CAREER RESPONSE\n Level: ", level)
        if level == 1:
            return("What do you want to become, when you grow up?", 2)
        
        if level == 2:
            res = get_secondary_response(input, "CAREER-1")
            print("RES: ", res)
            return(res)
            # if res == "UNKNOWN":
            #     return("I am sorry, I could not understand that", 0)
            # else:
            #     return(res, level+1)

# RETURN FAVORITE SUBJECT ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fav_subject_response(input, level):

    subject = {
        "MATH": ["I love math too! I am a big fan of calculus.", "Math is my favorite subject too!", "I love math! I really like the pythagorean theorem.", "I love math! I really like the quadratic formula.", "Math is so great!", "I agree, Math is amazing, and it forms the base of our world too!"],
        "SCIENCE": ["Science is so cool! I love learning about the human body.", "I love science too! I am a big fan of biology.", "I love science! I really like the human body.", "I love science! I really like the human brain.", "Science is so great!", "I agree, Science is amazing, and it forms the base of our world too!", "Science is so interesting!"],
        "ENGLISH": ["English is so cool! I love reading books.", "I love English too! I am a big fan of reading.", "I love English! I really like reading.", "I love English! I really like writing.", "English is so great!", "I agree, English is amazing, and it forms the base of our world too!", "English is so interesting!"],
        "SOCIAL STUDIES": ["Social Studies is so cool! I love learning about the world.", "I love Social Studies too! I am a big fan of history.", "I love Social Studies! I really like learning about the world.", "I love Social Studies! I really like learning about the past.", "Social Studies is so great!", "I agree, Social Studies is amazing, and it forms the base of our world too!", "Social Studies is so interesting!"],
        "HISTORY": ["History is so cool! I love learning about the past.", "I love History too! I am a big fan of history.", "I love History! I really like learning about the past.", "I love History! I really like learning about the past.", "History is so great!", "I agree, History is amazing, and it forms the base of our world too!", "History is so interesting!"],
        "GEOGRAPHY": ["Geography is so cool! I love learning about the world.", "I love Geography too! I am a big fan of geography.", "I love Geography! I really like learning about the world.", "I love Geography! I really like learning about the world.", "Geography is so great!", "I agree, Geography is amazing, and it forms the base of our world too!", "Geography is so interesting!"],
        "ART": ["Art is so cool! I love drawing.", "I love Art too! I am a big fan of drawing.", "I love Art! I really like drawing.", "I love Art! I really like drawing.", "Art is so great!", "I agree, Art is amazing, and it forms the base of our world too!", "Art is so interesting!"],
        "MUSIC": ["Music is so cool! I love listening to music.", "I love Music too! I am a big fan of music.", "I love Music! I really like listening to music.", "I love Music! I really like listening to music.", "Music is so great!", "I agree, Music is amazing, and it forms the base of our world too!", "Music is so interesting!"],
        "PHYSICAL EDUCATION": ["Physical Education is so cool! I love playing sports.", "I love Physical Education too! I am a big fan of sports.", "I love Physical Education! I really like playing sports.", "I love Physical Education! I really like playing sports.", "Physical Education is so great!", "I agree, Physical Education is amazing, and it forms the base of our world too!", "Physical Education is so interesting!"],
        "UNKNOWN": ["I haven't heard of that subject before!" "That is not a subject I am familiar with.", "Thats a new subject for me!"],
    }
    
    if level == 1:
        return("What is your favourite subject?", 2)

    if level == 2:

        response = get_secondary_response(input, "SUBJECT-1")
        
        if response != "UNKNOWN":
            response = random.choice(subject[response])

        return(response, 0)



# CHANGE THE LANGUAGE_________________________________________________________________________________________________________________________________________________________________________________________________
# def lang_change():

#     global curr_lang
#     global translator_human
#     global translator_bot

#     bot_response = "What language do you want to change to?"
            
#     bot_output(bot_response)
    
#     user_input = mic_input()
#     user_input = user_input.lower()
    
#     if user_input in languages:

#         bot_output("Changing language to", user_input, "... \nThis may take some time")
        
#         curr_lang = user_input

#         if curr_lang != 'english':
#             translator_human = Translator(languages[curr_lang] , 'en')
#             translator_bot = Translator('en', languages[curr_lang])
#             voices = engine.getProperty('voices')
#             for voice in voices:
#                 print(f"Voice: {voice.name}")
#             engine.setProperty('voice', voices[1].id)
        
#         else:
#             voices = engine.getProperty('voices')
#             for voice in voices:
#                 print(f"Voice: {voice.name}")
#             engine.setProperty('voice', voices[2].id)
    
#     else:
#         return("Sorry, I don't know that language yet")

#     return (f"Language changed to {curr_lang}")



# RECOGNIZE SIMPLE WORD PROBABLITIES

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0



# RECOGNIZE INTENTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_all_messages(message, code):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    if code == "YES/NO":
        response('YES', ["yes", "yea","sure","ok", "go ahead", "fine", "okay"], single_response=True)
        response('NO', ["no", "nope", "naw", "nah", "don't", "stop", "not", "no thanks", "no thank you", "no thanks", "not really"], single_response=True)
    
    elif code == "SUBJECT-1":
        print("\n\nSUBJECT-1\n\n")
        response('SCIENCE', ["Science", "scientific", "EVS", "Enviornmental sciences"], single_response=True)
        response('MATH', ["Math"], single_response=True)
        response('ENGLISH', ["English"], single_response=True)
        response('HISTORY', ["History"], single_response=True)
        response('GEOGRAPHY', ["Geography"], single_response=True)
        response('ART', ["Art"], single_response=True)
        response('MUSIC', ["Music"], single_response=True)
        response('PHYSICAL EDUCATION', ["Physical Education", "PE", "P.E.", "Sports"], single_response=True)
        response('FRENCH', ["French"], single_response=True)
        response('HINDI', ["Hindi"], single_response=True)
        response('SST', ["SST", "Social Science"], single_response=True)
        response('GK', ["GK"], single_response=True)
        response('COMPUTER', ["Computer"], single_response=True)
        response('BIOLOGY', ["Biology"], single_response=True)
        response('CHEMISTRY', ["Chemistry"], single_response=True)
        response('PHYSICS', ["Physics"], single_response=True)
        response('ECONOMICS', ["Economics"], single_response=True)
        response('POLITICAL SCIENCE', ["Political Science", "Civics"], single_response=True)
        response('DANCE', ["Dance"], single_response=True)
        response('MUSIC', ["Music"], single_response=True)
        response('DRAWING', ["Drawing"], single_response=True)
        response('PAINTING', ["Painting"], single_response=True)
        response('SANSKRIT', ["Sanskrit"], single_response=True)
    
    elif code == "CAREER-1":
        response('Some Response', ["doctor", "Doctor"], single_response=True)
            # response('ENGINEER', ["Engineer"], single_response=True)
            # response('POLICE', ["Police"], single_response=True)
            # response('TEACHER', ["Teacher"], single_response=True)
            # response('CIVIL SERVANT', ["Civil Servant"], single_response=True)
            # response('IAS OFFICER', ["IAS Officer"], single_response=True)
            # response('ARTIST', ["Artist"], single_response=True)
            # response('DANCER', ["Dancer"], single_response=True)
            # response('MUSICIAN', ["Musician"], single_response=True)
            # response('ARCHITECT', ["Architect"], single_response=True)
            # response('LAWYER', ["Lawyer"], single_response=True)
            # response('PHYSICIAN', ["Physician"], single_response=True)
            # response('PHARMACIST', ["Pharmacist"], single_response=True)
            # response('NURSE', ["Nurse"], single_response=True)
            # response('PSYCHOLOGIST', ["Psychologist"], single_response=True)
            # response('ACCOUNTANT', ["Accountant"], single_response=True)
            # response('BANKER', ["Banker"], single_response=True)
            # response('BUSINESSMAN', ["Businessman"], single_response=True)
            # response('BUSINESSWOMAN', ["Businesswoman"], single_response=True)

        
    

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return "UNKNOWN" if highest_prob_list[best_match] < 1 else best_match


# RECOGNIZE INTENTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_secondary_response(user_input, code):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message, code)
    return response




# PREPROCESSING DATA
def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence



def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))



# GETTING PREDICTIONS
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list



# GETTING RESPONSES
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return (result)



# MAIN FUNCTION THAT WORKS THE CODE OF THE RESPONSES
#I know I should have used a class or at least a switch for this but I was in a hurry

def check_response(sentence, code):
    # if sentence[:4] == "CODE":
    #     return ("lol", sentence)

    # else:
    #     return (sentence, 'NONE')
    return (sentence)



def chatbot_response(text):


    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    code = 'NONE'


    return check_response(res, 'NONE')



#BOT OUTPUT


def bot_output(bot_response):
    print("Bot:", bot_response)

    # if curr_lang != 'english':
    #     bot_response = translator_bot.translate([bot_response])[0]
    #     print("Bot (translated):", bot_response)
    
    # engine.say(bot_response)
    # engine.runAndWait()


 # TAKES THE MIC INPUT 

# def mic_input():


#     if 1 == 0:

#         global curr_lang
#         with mic as source:
#             r.adjust_for_ambient_noise(source)
#             print("\nListening...")
#             audio = r.listen(source)

#         user_input = r.recognize_google(audio, language = recognize_lang[curr_lang])
#         print("Thinking...")

#         print("\nYou:", user_input)

#         if curr_lang != 'english':
#             user_input = translator_human.translate([user_input])[0]
#             print("You (translated):", user_input)

#         user_input = translator_human.translate([user_input])[0]
#         print("\nYou (translated):", user_input)

#         return user_input
        
#     else:
#         user_input = input("You: ")
#         return user_input


# MAIN FUNCTION THAT RUNS THE CHATBOT

if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)

    # print("Input Device: ", p.get_device_info_by_index(mic.device_index))

    # translator_human = Translator('hi', 'en')
    # translator_bot = Translator('en', 'hi')

    while True:

        try:
            # user_input = mic_input()

            user_input = input("\nYou: ")
            
            bot_response = chatbot_response(user_input)
            
            bot_output(bot_response)
        
        except:
            print("No input recieved! Stopping recording")
            input()
        
        