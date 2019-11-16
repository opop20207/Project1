# -*- coding:utf-8 -*-
from __future__ import with_statement
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from contextlib import closing
import nltk
from konlpy.tag import Okt
import os
import json

#settings
DEBUG=True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('GPSR_SETTINGS', silent=True)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/result', methods=['GET','POST'])
def result():
    text = request.form['text']
    
    okt = Okt()
    temp = okt.morphs(text,stem=True)
    res = 0
    pointset = {"negative" : 0, "positive" : 0}
    wordset = {"negative" : [], "neutral" : [], "positive" : []}
    numset = {"total" : 0, "negative" : 0, "neutral" : 0, "positive" : 0}
    numset["total"] = len(temp)
    for s in temp:
        if s=='\r\n':
            continue
        s.strip(" ")
        with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
            data = json.load(f)
        flag = 0
        for i in range(0,len(data)):
            if data[i]['word'] == s:
                flag = 1
                pol = data[i]['polarity']
                pol_word = data[i]['word']
                pol = int(pol)
                res = res+pol
                if pol<0:
                    wordset["negative"].append(pol_word)
                    numset["negative"] = numset["negative"] + 1
                    pointset["negative"] = pointset["negative"] + pol
                elif pol==0:
                    wordset["neutral"].append(pol_word)
                    numset["neutral"] = numset["neutral"] + 1
                elif pol>0:
                    wordset["positive"].append(pol_word)
                    numset["positive"] = numset["positive"] + 1
                    pointset["positive"] = pointset["positive"] + pol
        
        if flag == 0:
            wordset["neutral"].append(s)
            numset["neutral"] = numset["neutral"] + 1
                 
    return render_template('result.html',res=res,wordset = wordset, numset = numset, pointset = pointset)

if __name__ == '__main__' :
    app.run()