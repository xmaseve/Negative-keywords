# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:54:27 2016

@author: Qi Yi
"""

'''
Before import Excel file into Python, please delete the total row in the search
term report, and use pivot table because there are some duplications in the report.
For pivot table, you only need to choose search term, cost and converted clicks.
Copy the result of pivot table and paste it in the new Excel file.
'''

import pandas as pd
import re 
import numpy as np
from textblob import TextBlob

#python -m textblob.download_corpora
#change your direction according to your needs. 
searchterm = pd.read_csv('C:\Users\Qi Yi\Desktop\searchterm.csv')
searchterm.head()

term = searchterm[["Row Labels", "Cost", "Converted clicks"]]
term.head()
term.describe()
data = term.values.tolist()
terms = term["Row Labels"]

#stopwords = ["in","for", "of", "a", "an", "the"]

def preprocess(data):
    cleantext = []
    for row in range(len(data)):
        letters_only = re.sub("[^a-zA-Z]", " ", data[row][0])
        words=letters_only.split()
        #stop=set(stopwords.words('english'))
        #meanfulwords=[w for w in words if not w in stopwords]
        cleantext.append(words)
    return cleantext

cleantext=preprocess(data)

def createVocabList(cleantext):
    vocabSet = set([])
    for i in cleantext:
        vocabSet = vocabSet | set(i)
    vocabList = list(vocabSet)
    return vocabList

def wordFrequency(vocabList, cleantext):
    frequency = []
    for word in vocabList:
        count = 0
        for i in range(len(cleantext)):
            if word in cleantext[i]:            
                count += 1
        frequency.append(count)
    return frequency
    
vocabList = createVocabList(cleantext)
frequency = wordFrequency(vocabList, cleantext)
data1 = pd.DataFrame(vocabList, columns=["Term"])
data1["Count"] = frequency
#data1 = data1.sort(["Count"], ascending=[False])

def calculate(vocabList, data, cleantext):    
    costs = []
    convs = []

    for word in vocabList:
        cost = 0
        conv = 0
        for i in range(len(data)):
            if word in cleantext[i]:
                cost += data[i][1]
            if word in cleantext[i] and data[i][2] > 0:
                conv += data[i][2]
        costs.append(cost)
        convs.append(conv)
    return costs, convs

costs, convs = calculate(vocabList, data, cleantext)
data1["Costs"] = costs
data1["Conversions"] = convs
comb = data1.values.tolist()

def noconvCost(comb):
    ncosts = 0
    for i in range(len(comb)):  
        if comb[i][3] == 0:
            ncosts += comb[i][2]
    return ncosts

ncosts = noconvCost(comb)

def compute(comb, convs, costs, ncosts):
    weights = []
    for i in range(len(comb)):
        if comb[i][3] > 0:
            weight = float(comb[i][3]) / sum(convs)
            weights.append(weight)
        elif comb[i][3] == 0:
            one = -comb[i][2] / np.sum(ncosts)
            two = float(np.max(convs)) / np.sum(convs)
            weight = one / two
            weights.append(weight)
    return weights
    
weights = compute(comb, convs, costs, ncosts)
data1["Weights"] = weights     
neg_keyword = data1.sort_values(["Weights"], ascending=True)   
df = data1.values.tolist()

'''
def output(terms, df):
    result = []
    for i in terms:
        score = 0
        for j in range(len(df)):
            if df[j][0] in i:
                score += df[j][4]
        result.append(score)
    return result

result = output(terms, df)
searchterm["result"] = result
'''
newdata = searchterm.values.tolist()

'''
Remove the existing keywords from the search terms.
'''

keywords = pd.read_csv('C:\Users\Qi Yi\Desktop\keywords.csv')
keywords = keywords.values.tolist()

def existing(keywords):
    cleanwords = []
    for i in range(len(keywords)):
        words = re.sub(r"[^\w]", " ", keywords[i][0]).strip()
        words = " ".join(words.split())
        cleanwords.append(words)
    cleanwords = list(set(cleanwords))
    return cleanwords
    
cleanwords = existing(keywords)

def newkeywords(data, cleanwords):
    new = []
    for i in range(len(data)):
        if data[i][0] not in cleanwords:
            new.append(data[i])
    return new
            
new = newkeywords(data, cleanwords)

'''
PICKLE = "averaged_perceptron_tagger.pickle"
AP_MODEL_LOC = 'file:'+str(find('taggers/averaged_perceptron_tagger/'+PICKLE))
tagger = PerceptronTagger(load=False)
tagger.load(AP_MODEL_LOC)
pos_tag = tagger.tag
'''


def negPhrase(new):
    adj = ["JJ", "JJR", "JJS"]
    noun = ["NN", "NNS", "NNP", "NNPS"]
    verb = ["VB", "VBZ", "VBP", "VBD", "VBN"]

    phrases = []
    for i in range(len(new)):
        blob = TextBlob(new[i][0])
        tags = blob.tags
        for j in range(len(tags)):
            if j + 1 <= len(tags) - 1:
                if (tags[j][1] in adj or noun or verb) and (tags[j+1][1] in noun):
                    phrases.append(tags[j][0] + " " + tags[j+1][0])
                else:
                    break
    phrases = list(set(phrases))
    return phrases

phrases = negPhrase(new)
    
def output(phrases, df):
    result = []
    for i in phrases:
        score = 0
        for j in range(len(df)):
            if df[j][0] in i:
                score += df[j][4]
        result.append(score)
    return result

result = output(phrases, df)            
        
neg_phrases = pd.DataFrame(phrases, columns=["Phrases"])
neg_phrases["Result"] = result
neg_phrases = neg_phrases.sort_values(["Result"], ascending = True)


'''
searchterm["result"] = result
searchterm.to_csv('C:\\Users\\Qi Yi\\Desktop\\new search term.csv')
positive = searchterm.sort(["result"], ascending=False)
positive30 = positive.head(30)
positive30.to_csv('C:\\Users\\Qi Yi\\Desktop\\positive keywords.csv')
negative = searchterm[searchterm.result < 0]
negative = negative.sort(["result"], ascending=True)
negative.to_csv('C:\\Users\\Qi Yi\\Desktop\\negative keywords.csv')
'''
neg_keyword.to_csv('C:\\Users\\Qi Yi\\Desktop\\negative keywords.csv')
neg_phrases.to_csv('C:\\Users\\Qi Yi\\Desktop\\negative phrases.csv')
