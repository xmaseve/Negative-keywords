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

#change your direction according to your needs. 
searchterm = pd.read_csv('C:\Users\Qi Yi\Desktop\searchterm.csv')
searchterm.head()

term = searchterm[["Row Labels", "Cost", "Converted clicks"]]
term.head()
term.describe()
data = term.values.tolist()
terms = term["Row Labels"]

stopwords = ["in","for", "of", "a", "an", "the"]

def preprocess(data):
    cleantext = []
    for row in range(len(data)):
        letters_only = re.sub("[^a-zA-Z]", " ", data[row][0])
        words=letters_only.split()
        #stop=set(stopwords.words('english'))
        meanfulwords=[w for w in words if not w in stopwords]
        cleantext.append(meanfulwords)
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
    
terms = term["Row Labels"]  
#terms = terms.values.tolist()      
new = data1.values.tolist()

def output(terms, new):
    result = []
    for i in terms:
        score = 0
        for j in range(len(new)):
            if new[j][0] in i:
                score += new[j][4]
        result.append(score)
    return result

result = output(terms, new)

searchterm["result"] = result
searchterm.to_csv('C:\\Users\\Qi Yi\\Desktop\\new search term.csv')
positive = searchterm.sort(["result"], ascending=False)
positive30 = positive.head(30)
positive30.to_csv('C:\\Users\\Qi Yi\\Desktop\\positive keywords.csv')
negative = searchterm[searchterm.result < 0]
negative = negative.sort(["result"], ascending=True)
negative.to_csv('C:\\Users\\Qi Yi\\Desktop\\negative keywords.csv')



