# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:05:52 2016

@author: Qi Yi
"""


import pandas as pd
import re

keywords = pd.read_csv('C:\Users\Qi Yi\Desktop\Keyword report.csv') #Change your filepath
searchquery = pd.read_csv("C:\Users\Qi Yi\Desktop\Search term report.csv") #Change your filepath
keywords = keywords[["Campaign", "Ad group", "Keyword"]]
searchquery = searchquery[["Campaign", "Ad group", "Search term", "Cost", "Conversions"]]

keywords = keywords.values.tolist()

'''
process search term report to slice adgroup data from each campaign
'''
campaign = list(searchquery["Campaign"].unique())
campaign.sort()
len(campaign)
searchterms = searchquery.values.tolist()

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
    
def seperate_column(a):
    cost = []
    convs = []
    for row in a:
        cost.append(row[0])
        convs.append(row[1])
    return cost, convs
 
scan = []    
topwords = []
for i in campaign:
    
    term_campdata = campData(searchterms, i) #change the number to change the campaign
    term_campdata = pd.DataFrame(term_campdata, columns=["Campaign", "Ad group", "Search term", "Cost", "Conversions"])
    adgroup = list(term_campdata["Ad group"].unique())
    adgroup.sort()
    term_campdata = term_campdata.values.tolist()
    kw_campdata = campData(keywords, i)
    
    
    for j in adgroup:
        
        #process search term report to slice adgroup data from each campaign

        term_adgroupdata = adgroupData(term_campdata, j)
        term_adgroupdata = pd.DataFrame(term_adgroupdata, columns=["Campaign", "Ad group", "Search term", "Cost", "Conversions"])
        searchterm = list(term_adgroupdata["Search term"].unique())
        searchterm.sort()

        #Find the most frequent words in the keywords list
        kw_adgroupdata = adgroupData(kw_campdata, j)
        cleanwords = existing(kw_adgroupdata)
        words = split_word(cleanwords)
        kwList = createVocabList(words)
        frequency = wordFrequency(kwList, words)
        count = pd.DataFrame(kwList, columns=["Words"])
        count["Frequency"] = frequency
        count = count.sort_values(["Frequency"], ascending=False)
        top3 = count.Words.head(3) #change the number of top words
        top3 = top3.values.tolist()
        top3.append('rent')  #add a new element into the top3 list
        top4 = '|'.join(map(re.escape, top3))
        topwords.append(i + ":" + j + "-" + str(top3))
           
        scan.append(term_adgroupdata[~(term_adgroupdata["Search term"].str.contains(top4))]) 

        
unmatch = pd.concat(scan) 
topwords = pd.DataFrame(topwords, columns=["Top words"]) 
#topwords.to_csv("C:\\Users\\Qi Yi\\Desktop\\Top words.csv")   #Change your filepath
unmatch.to_csv("C:\\Users\\Qi Yi\\Desktop\\output.csv") #Change your filepath




