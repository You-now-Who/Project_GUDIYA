import tensorflow as tf
import numpy as np
import re
from nltk.tokenize import word_tokenize
import nltk
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
# import responses
# from responses import conv_res

unique_intents = ['GREETINGS', 'CONVERSATION', 'STEM']

model = tf.keras.models.load_model('intent.h5')

with open('tokenizer.pickle', 'rb') as handle:
    word_tokenizer = pickle.load(handle)

def padding_doc(encoded_doc, max_length):
  return(pad_sequences(encoded_doc, maxlen = max_length, padding = "post"))


def predictions(text):
  max_length = 1000
  clean = re.sub(r'[^ a-z A-Z 0-9]', " ", text)
  test_word = word_tokenize(clean)
  test_word = [w.lower() for w in test_word]
  test_ls = word_tokenizer.texts_to_sequences(test_word)
  print(test_word)
  #Check for unknown words
  if [] in test_ls:
    test_ls = list(filter(None, test_ls))
    
  test_ls = np.array(test_ls).reshape(1, len(test_ls))
 
  x = padding_doc(test_ls, max_length)
  
  pred = model.predict(x)
  
  
  return pred

def get_final_output(text):

  pred = predictions(text)
  all_predictions = pred[0]
 
  classes = np.array(unique_intents)
  ids = np.argsort(-all_predictions)
  classes = classes[ids]
  all_predictions = -np.sort(-all_predictions)
  

  # for i in range(pred.shape[1]):
  #   print("%s has confidence = %s" % (classes[i], (all_predictions[i])))

  return(classes[np.where(all_predictions == max(all_predictions))])





# model.predict('Lol')

# text = "how are you feeling today"
# pred = predictions(text)
# print(responses.conv_res(text))