# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:21:42 2016

@author: Qi Yi
"""

import pandas as pd
import re

keywords = pd.read_excel(r'C:\Users\Qi Yi\Desktop\SV_Keyword_report.xlsx') #Change your filepath
searchquery = pd.read_excel("C:\Users\Qi Yi\Desktop\SV_campus_search_term.xlsx") #Change your filepath
keywords = keywords[["Campaign", "Ad group", "Keyword"]]
searchquery = searchquery[["Campaign", "Ad group", "Search term", "Cost", "Converted clicks"]]

keywords = keywords.values.tolist()

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
    
def campaign_level(keywords, n):
    
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
    
top5, unmatched = campaign_level(keywords, 5)
top = [str(top5)]
#multiple sheets in the Excel file  
writer = pd.ExcelWriter("C:\\Users\\Qi Yi\\Desktop\\campagin_level.xlsx")      
topwords = pd.DataFrame(top, columns=["Top words"]) 
topwords.to_excel(writer, "Top words")  
unmatched.to_excel(writer, "Search terms") 
writer.save()
