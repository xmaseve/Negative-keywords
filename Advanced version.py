# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:05:52 2016

@author: Qi Yi
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 09:11:05 2016

@author: Qi Yi
"""

import pandas as pd
import re

keywords = pd.read_csv('C:\Users\Qi Yi\Desktop\Keyword report.csv')
searchquery = pd.read_csv("C:\Users\Qi Yi\Desktop\Search term report.csv")
keywords = keywords[["Campaign", "Ad group", "Keyword"]]
searchquery = searchquery[["Campaign", "Ad group", "Search term", "Cost", "Conversions"]]

keywords = keywords.values.tolist()

'''
process keyword report to slice adgroup data from each campaign
'''
df = searchquery[searchquery.columns[[0,1,2]]]
campaign = list(df["Campaign"].unique())
campaign.sort()
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

def existing(keywords):
    cleanwords = []
    for i in range(len(keywords)):
        words = re.sub(r"[^\w]", " ", keywords[i][2]).strip() #keyword column
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
    
def seperate(a):
    cost = []
    convs = []
    for row in a:
        cost.append(row[0])
        convs.append(row[1])
    return cost, convs
 
scan = []    
topwords = []
for i in campaign:
    
    term_campdata = campData(df, i) #change the number to change the campaign
    term_campdata = pd.DataFrame(term_campdata, columns=["Campaign", "Ad group", "Search term"])
    adgroup = list(term_campdata["Ad group"].unique())
    adgroup.sort()
    term_campdata = term_campdata.values.tolist()
    kw_campdata = campData(keywords, i)
    
    
    for j in adgroup:
        
        #process search term report to slice adgroup data from each campaign

        #search = searchquery.values.tolist()
        #term_camp1 = campData(search, i) 
        term_adgroupdata = adgroupData(term_campdata, j)
        term_adgroupdata = pd.DataFrame(term_adgroupdata, columns=["Campaign", "Ad group", "Search term"])
        #searchterm1 = list(term_adgroupdata["Search term"].unique())
        #searchterm1.sort()

        #a = adgroupdata.groupby(["Search term"]).sum()
        #a = a.values.tolist()

        #cost, convs = seperate(a)

        #new_adgroup1 = pd.DataFrame(searchterm1, columns=["Row Labels"])
        #new_adgroup1["Cost"] = cost
        #new_adgroup1["Conversions"] = convs

        #data = adgroupdata.values.tolist()
        #terms = new_adgroup1["Row Labels"]
        #adgroup1 = adgroupData(camp1, j)

        #Find the most frequent words in the keywords list
        kw_adgroupdata = adgroupData(kw_campdata, j)
        cleanwords = existing(kw_adgroupdata)
        words = split_word(cleanwords)
        kwList = createVocabList(words)
        frequency = wordFrequency(kwList, words)
        count = pd.DataFrame(kwList, columns=["Words"])
        count["Frequency"] = frequency
        count = count.sort_values(["Frequency"], ascending=False)
        top3 = count.Words.head(3)
        top3 = top3.values.tolist()
        #print top3
        
        topwords.append(i + ":" + j + "-" + str(top3))
           
        scan.append(term_adgroupdata[~(term_adgroupdata["Search term"].str.contains('top[0]'))])
     
a = pd.concat(scan)  
topwords.to_csv("C:\\Users\\Qi Yi\\Desktop\\Top words.csv")   
a.to_csv("C:\\Users\\Qi Yi\\Desktop\\output1.csv")


