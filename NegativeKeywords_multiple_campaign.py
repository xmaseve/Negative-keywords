# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:45:32 2016

@author: Qi Yi
"""

import pandas as pd
import re
from pandas import ExcelWriter


keywords = pd.read_excel(r'C:\Users\Qi Yi\Desktop\Keyword_report.xlsx') #Change your filepath
searchquery = pd.read_excel("C:\Users\Qi Yi\Desktop\Search_term_report.xlsx") #Change your filepath
keywords = keywords[["Campaign", "Ad group", "Keyword"]]
searchquery = searchquery[["Campaign", "Ad group", "Search term", "Cost", "Conversions"]]

'''
Only North America Market
'''
searchquery_NA = searchquery[searchquery["Campaign"].str.contains("NA")]
keywords_NA = keywords[keywords["Campaign"].str.contains("NA")]

keywords = keywords.values.tolist()

'''
process search term report to slice adgroup data from each campaign
'''
campaign = list(searchquery_NA["Campaign"].unique())
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

def campaign_level(searchquery, keywords, n):
    
    cleanwords = existing(keywords)
    words = split_word(cleanwords)
    kwList = createVocabList(words)
    frequency = wordFrequency(kwList, words)
    count = pd.DataFrame(kwList, columns=["Words"])
    count["Frequency"] = frequency
    count = count.sort_values(["Frequency"], ascending=False)
    topN = count.Words.head(n) #change the number of top words
    topN = topN.values.tolist()
    #top3.append('rent')  #add a new element into the top3 list
    top = '|'.join(map(re.escape, topN))
           
    unmatched = searchquery[~(searchquery["Search term"].str.contains(top))]
    return top, unmatched
    
def multiple_campaign(campaign, searchterms, searchquery, keywords, n):    
       
    topwords= []
    negative = [] 

    for i in campaign:
    
        term_campdata = campData(searchterms, i) #change the number to change the campaign
        term_campdata = pd.DataFrame(term_campdata, columns=["Campaign", "Ad group", "Search term", "Cost", "Converted clicks"])
        kw_campdata = campData(keywords, i)
        t, neg = campaign_level(term_campdata, kw_campdata, n)
        topwords.append(i + ":" + str(t))
        negative.append(neg)
        
    return topwords, negative
            
topwords, negative = multiple_campaign(campaign, searchterms, searchquery_NA, keywords, 5)


#multiple sheets in the Excel file  
writer = ExcelWriter("C:\\Users\\Qi Yi\\Desktop\\campaign level.xlsx") #change the file path 
unmatch = pd.concat(negative) 
topwords = pd.DataFrame(topwords, columns=["Top words"]) 
topwords.to_excel(writer, "Top words")  
unmatch.to_excel(writer, "Search terms") 
writer.save()




