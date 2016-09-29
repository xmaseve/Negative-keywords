# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:54:27 2016

@author: Qi Yi
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import re 
import numpy as np


searchterm = pd.read_csv('C:\Users\Qi Yi\Desktop\searchterm.csv')
searchterm.head()

term = searchterm[["Search term", "Cost", "Converted clicks"]]
term.head()
term.describe()

'''
df = term.pivot_table(index=["Search term"], aggfunc="sum")
'''

data = term.values.tolist()

def preprocess(data):
    cleantext = []
    for row in range(len(data)):
        letters_only = re.sub("[^a-zA-Z]", " ", data[row][0])
        words=letters_only.split()
        #stop=set(stopwords.words('english'))
       # meanfulwords=[w for w in words if not w in stop]
        cleantext.append(words)
    return cleantext

cleantext=preprocess(data)

def createVocabList(cleantext):
    vocabSet = set([])
    for i in cleantext:
        vocabSet = vocabSet | set(i)
    vocabList = list(vocabSet)
    return vocabList

def bagOfWords2Vec(vocabList, inputset):
    returnVec = [0] * len(vocabList)
    for word in inputset:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec
    
vocabList = createVocabList(cleantext)

costs = []
convs = []

for word in vocabList:
    cost = 0
    conv = 0
    for i in range(len(data)):
        if word in data[i][0]:
            cost += data[i][1]
            conv += data[i][2]
    costs.append(cost)
    convs.append(conv)
print costs
print convs
  
df = pd.DataFrame(costs, columns=["Costs"])
df["Convs"] = convs

comb = df.values.tolist()

weights = []
for row in comb:
    if row[1] > 0:
        weight = float(row[1]) / np.sum(convs)
        weights.append(weight)
    elif row[1] == 0:
        weight = - row[0] / np.sum(costs) / np.max(convs) / np.sum(convs)
        weights.append(weight)

df1 = pd.DataFrame(vocabList, columns=["Word"])
df1["Weights"] = weights
terms = term["Search term"]  
terms = terms.value.tolist()      

new = df1.values.tolist()

result = []
for i in terms:
    score = 0
    for j in range(len(new)):
        if new[j][0] in i:
                score += new[j][1]
    result.append(score)




