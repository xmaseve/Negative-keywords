# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 09:11:05 2016

@author: Qi Yi
"""

import pandas as pd
import re

keywords = pd.read_excel(r"C:\Users\Qi Yi\Desktop\7 Day Keyword List 10.05..xlsx", sheetname="Keyword report (41)")
searchquery = pd.read_excel(r"C:\Users\Qi Yi\Desktop\7 Day SQ Report 10.05.16.xlsx")

'''
process keyword report to slice adgroup data from each campaign
'''
df = keywords[keywords.columns[[0,1,2]]]
campaign = list(df["Campaign"].unique())
len(campaign)
df = df.values.tolist()

def campData(df, CampName):
    camp = []
    for i in range(len(df)):
        if df[i][0] == CampName:
            camp.append(df[i])
    return camp

def adgroupData(campdata, adgroupName):
    group = []
    for i in range(len(campdata)):
        if campdata[i][1] == adgroupName:
            group.append(campdata[i])
    return group

camp1 = campData(df, campaign[0]) #change the number to change the campaign
camp1 = pd.DataFrame(camp1, columns=["Campaign", "Ad group", "Keyword"])
adgroup = list(camp1["Ad group"].unique())
len(adgroup)
adgroup
camp1 = camp1.values.tolist()    
adgroup1 = adgroupData(camp1, adgroup[1]) #change the number to change the ad group
len(adgroup1)

'''
Find the most frequent words in the keywords list
'''

def existing(keywords):
    cleanwords = []
    for i in range(len(keywords)):
        words = re.sub(r"[^\w]", " ", keywords[i][2]).strip()
        words = " ".join(words.split())
        cleanwords.append(words)
    cleanwords = list(set(cleanwords))
    return cleanwords

def split_word(cleanwords):
    words = []
    for term in cleanwords:
        word = term.split()
        words.append(word)
    return words
    
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
    
cleanwords = existing(adgroup1)
words = split_word(cleanwords)
kwList = createVocabList(words)
frequency = wordFrequency(kwList, words)

count = pd.DataFrame(kwList, columns=["Words"])
count["Frequency"] = frequency
count = count.sort_values(["Frequency"], ascending=False)
top5 = count.Words.head()
top5 = top5.values.tolist()
top5


'''
process search term report to slice adgroup data from each campaign
'''

searchquery = searchquery[["Campaign", "Ad group", "Search term", "Cost", "Conversions"]]
search = searchquery.values.tolist()

term_camp1 = campData(search, campaign[0]) #change the number to change the campaign
term_adgroup1 = adgroupData(term_camp1, adgroup[1]) ##change the number to change the ad group

term_adgroup1 = pd.DataFrame(term_adgroup1, columns=["Campaign", "Ad group", "Search term", "Cost", "Conversions"])
searchterm1 = list(term_adgroup1["Search term"].unique())
searchterm1.sort()
len(searchterm1)

a = term_adgroup1.groupby(["Search term"]).sum()
a = a.values.tolist()

def seperate(a):
    cost = []
    convs = []
    for row in a:
        cost.append(row[0])
        convs.append(row[1])
    return cost, convs

cost, convs = seperate(a)

new_adgroup1 = pd.DataFrame(searchterm1, columns=["Row Labels"])
new_adgroup1["Cost"] = cost
new_adgroup1["Conversions"] = convs

data = new_adgroup1.values.tolist()
terms = new_adgroup1["Row Labels"]
           
new_adgroup1[~new_adgroup1["Row Labels"].str.contains('speaker')]


