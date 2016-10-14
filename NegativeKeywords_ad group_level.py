# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:05:52 2016

@author: Qi Yi
"""


import pandas as pd
import re
from pandas import ExcelWriter

'''
keywords = pd.read_csv('C:\Users\Qi Yi\Desktop\Keyword report.csv') #Change your filepath
searchquery = pd.read_csv("C:\Users\Qi Yi\Desktop\Search term report.csv") #Change your filepath
keywords = keywords[["Campaign", "Ad group", "Keyword"]]
searchquery = searchquery[["Campaign", "Ad group", "Search term", "Cost", "Conversions"]]

keywords = keywords.values.tolist()
'''
keywords = pd.read_excel(r'C:\Users\Qi Yi\Desktop\SV_Keyword_report.xlsx') #Change your filepath
searchquery = pd.read_excel("C:\Users\Qi Yi\Desktop\SV_campus_search_term.xlsx") #Change your filepath
keywords = keywords[["Campaign", "Ad group", "Keyword"]]
searchquery = searchquery[["Campaign", "Ad group", "Search term", "Cost", "Converted clicks"]]

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

def adgroup_level(campaign, searchterms, n):    
    scan = []    
    topwords = []
    for i in campaign:
    
        term_campdata = campData(searchterms, i) #change the number to change the campaign
        term_campdata = pd.DataFrame(term_campdata, columns=["Campaign", "Ad group", "Search term", "Cost", "Converted clicks"])
        adgroup = list(term_campdata["Ad group"].unique())
        adgroup.sort()
        term_campdata = term_campdata.values.tolist()
        kw_campdata = campData(keywords, i)
    
    
        for j in adgroup:
        
        #process search term report to slice adgroup data from each campaign

            term_adgroupdata = adgroupData(term_campdata, j)
            term_adgroupdata = pd.DataFrame(term_adgroupdata, columns=["Campaign", "Ad group", "Search term", "Cost", "Converted clicks"])
            searchterm = list(term_adgroupdata["Search term"].unique())
            searchterm.sort()
        '''
        a = term_adgroupdata.groupby(["Search term"]).sum()
        a = a.values.tolist()

        cost, convs = seperate_column(a)

        new_adgroup = pd.DataFrame(searchterm, columns=["Search term"])
        new_adgroup["Cost"] = cost
        new_adgroup["Conversions"] = convs
        '''
        #Find the most frequent words in the keywords list
            kw_adgroupdata = adgroupData(kw_campdata, j)
            cleanwords = existing(kw_adgroupdata)
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
            topwords.append(i + ":" + j + "-" + str(topN))
           
            scan.append(term_adgroupdata[~(term_adgroupdata["Search term"].str.contains(top))]) 
    return scan, topwords
    
scan, topwords = adgroup_level(campaign, searchterms, 3)

#multiple sheets in the Excel file  
writer = ExcelWriter("C:\\Users\\Qi Yi\\Desktop\\Ad group level.xlsx")      
unmatch = pd.concat(scan) 
topwords = pd.DataFrame(topwords, columns=["Top words"]) 
topwords.to_excel(writer, "Top words")  
unmatch.to_excel(writer, "Search terms") 
writer.save()




