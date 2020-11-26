import os
import re
import pandas as pd
import numpy as np
import subprocess
from subprocess import PIPE, Popen
import flask
import pickle
from flask import Flask, request, redirect, render_template

from nltk.tokenize import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from deeppavlov import build_model, configs

from sklearn.neighbors import KNeighborsClassifier
import string


punctuation = string.punctuation


sent_model = build_model(configs.classifiers.rusentiment_elmo_twitter_cnn, download=True)
ner_model = build_model(configs.ner.ner_rus, download=True)

model_analyst = pickle.load(open(os.path.join('models','analyst.pkl'), 'rb'))
model_empath = pickle.load(open(os.path.join('models','empath.pkl'), 'rb'))
model_expert = pickle.load(open(os.path.join('models','expert.pkl'), 'rb'))
model_fighter = pickle.load(open(os.path.join('models','fighter.pkl'), 'rb'))
model_leader = pickle.load(open(os.path.join('models','leader.pkl'), 'rb'))
model_performer = pickle.load(open(os.path.join('models','performer.pkl'), 'rb'))

models = [model_analyst, model_empath, model_expert, model_fighter, model_leader, model_performer]
architypes = ['Аналитик', 'Эмпат', 'Эксперт', 'Боец', 'Вождь', 'Исполнитель']

def do_sentiment(line):
    return sent_model([line])[0]

def find_ner(line):
    words, tags = ner_model([line])
    try:
        for w, t in zip(words[0], tags[0]):
            if t != 'O':
                return 1
            else:
                return 0
    except:
        return 0

def preprocess(text):
    data = pd.DataFrame({'text':[text]})
    # initialize snetiment features, then add 1 according to the detected sentiment
    data['sentiment_negative_mean']=0
    data['sentiment_neutral_mean']=0
    data['sentiment_positive_mean']=1
    data['sentiment_skip_mean']=0
    data['sentiment_speech_mean']=0
    data['ner_mean'] = data['text'].apply(find_ner)

    sentiment = do_sentiment(data['text'].values[0])
    for col in data.columns.tolist():
        if sentiment in col:
            data[col] += 1

    data["answer_len_mean"] = data['text'].apply(len)
    data['upper_case_word_count_mean'] = data['text'].apply(lambda x: len([wrd for wrd in x.split() if wrd[0].isupper()]))
    data['punctuation_count_mean'] = data['text'].apply(lambda x: len("".join(_ for _ in x if _ in punctuation)))

    print(data)
    return data.drop('text',axis=1)


def predict(text):
    features = preprocess(text)
    type_dict = {type:model.predict_proba(features)[:,1][0] for model, type in zip(models, architypes)}
    type_sorted = {k: v for k, v in sorted(type_dict.items(), key=lambda item: item[1], reverse=True)}
    types = []
    for k, v in zip(type_sorted.keys(), type_sorted.values()):
        types.append(k+' '+str(int(round(v*100)))+'%')
    return types[:3]


def recommend_course(types):
    """Как первое приближение рекомендации по жестко заданному словарю Архетип:список курсов"""
    top_type = types[0].split(' ')[0]
    if top_type == 'Аналитик':
        links = ['www.edx.org/course/data-analysis-in-power-bi', 'www.edx.org/course/analyzing-data-with-python']
        names = ['Analyzing and Visualizing Data with Power BI', 'Analyzing Data with Python от IBM']
        courses = zip(links, names)
    elif top_type == 'Вождь':
        links = ['www.coursera.org/learn/uva-darden-project-management', 'pmclub.pro/courses/pm-101']
        names = ['Основы планирования и управления проектом', 'Бесплатный курс по управлению проектами']
        courses = zip(links, names)
    # TO DO: дополнить словарь мэтчами Архетип:курсы для оставшихся типов.
    else:
        links = ['www.coursera.org/learn/problem-solving','edx.org/course/philosophy-and-critical-thinking']
        names = ['Эффективное решение проблем и принятие решений','Philosophy and Critical Thinking']
        courses = zip(links, names)
    return courses
