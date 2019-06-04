

from urllib.request import urlopen
from urllib.error import URLError
import ssl, re , time

import requests
from bs4 import BeautifulSoup

def urlexists(submitted_url):
    
    a = ssl.SSLContext()
    a.check_hostname = False
    a.verify_mode = ssl.CERT_NONE
    try:
        urlopen(submitted_url, context=a)
        
        is_url = True
        return is_url

    except URLError as e:
        is_url = False
        return is_url


def profileKeywords(keyword_search_raw):
    
    #print ('profile keywords')

    keyword_list_raw = keyword_search_raw.split(',')
    keyword_list_profiled = []
    for word in keyword_list_raw:
        kword = str(word).lstrip().rstrip()
        if len(kword) > 1:
            keyword_list_profiled.append(kword)
    
    count_keywords =  (len(keyword_list_profiled))
    return keyword_list_profiled, count_keywords
    


def validKeywords(keyword_list_profiled):
    
    #print ('check if keywords are valid')    
    minimum_keywords = 5
    maximum_keywords = 10
    #Count keywords to ensure 5 as a minimum been entered and no more than 10
    #Does not exceed database field length

    if len(keyword_list_profiled) >= minimum_keywords and len(keyword_list_profiled) <= maximum_keywords:
        return True
    else:
        return False

def scrapeWebsite(keywords,submitted_url):
 
    soup = getSoup(submitted_url)

    p_tag = soup.find_all('p')
    
    
    results = []
    sumOfWordCount = 0

    for word in keywords:
        wordCount = 0    
        for p in p_tag:
            temp_counter = 0
            _ ,  temp_counter =  re.subn(word, '',str(p),flags=re.I)
            wordCount = wordCount + temp_counter
        
        results.append([word,wordCount])
        sumOfWordCount = sumOfWordCount + wordCount

    keyword_match_results = results

    totalWordCount = 0
    for p in p_tag:

        tempTotalWordCount = len(re.findall(r'\w+', str(p.text)))
        totalWordCount = totalWordCount + tempTotalWordCount

    
    occurrence_percent = round(((sumOfWordCount * 1.0) / totalWordCount) * 100,3)
    '''
        print ('Total word count ', totalWordCount)
        print ('Sum of word count ', sumOfWordCount)
        print ('Word count occurrence % ', occurrence_percent)
    '''

    return {'totalWordCount': totalWordCount, 'sumOfWordCount': sumOfWordCount,'occurrence_percent' : occurrence_percent, 
    'keyword_match_results': keyword_match_results}





def getAlexaResults(site):

    ALEXA_URL = 'https://www.alexa.com/siteinfo/' + site
    #+ site
    soup = getSoup(ALEXA_URL)    
    
    strong_tag = soup.findAll('strong',{'class':'metrics-data align-vmiddle'})
    
    alexa_results = []
    alexa_result_titles = ['Global Rank','Country Rank','Bounce Rate','Daily Page Views','Daily Time Spent', 'Search Visits']
    


    for index , title in enumerate(alexa_result_titles):
        value = str(strong_tag[index].text).lstrip().rstrip().replace('\n','')

        if title != 'Bounce Rate' and title != 'Search Visits':
            value_cleaned =  int(re.sub('[^A-Za-z0-9]+', '', value))
            value = value_cleaned

        alexa_results.append([title , value])

    return alexa_results

def webSearch(searchEngine,keyword_list):   

    words = ''
    for word in keyword_list:
        words += word + '+and+'
        
    search_word = (words[0:len(words)-5])
    

    if searchEngine == 'Bloomberg':

        current_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        advanceSearch = '&startTime=-1d&endTime='
        searchLast24hr = advanceSearch + current_time

        bloombergURL = 'https://www.bloomberg.com/search?query=' + search_word + searchLast24hr
        
        bloomberg_results = (getSearchResults(searchEngine , bloombergURL, keyword_list))
        return bloomberg_results
        
    elif searchEngine == 'Reuters':
        searchPastDay = '&sortBy=relevance&dateRange=pastDay'
        reutersURL = "https://uk.reuters.com/search/news?blob=" + search_word + searchPastDay
        # print('LLLLLLLLLLLLLLLLL')
        print (reutersURL)
        reuters_results =  (getSearchResults(searchEngine , reutersURL , keyword_list))
        return reuters_results
    else:
        return 'No Results'

def getSoup(urllink):
    try:
        r = requests.get(urllink)
        soup = BeautifulSoup(r.content,  "html.parser")
        return soup
    except requests.exceptions.RequestException as err:
        return err
    

def getSearchResults(searchEngine , searchURL, keyword_list):
    
    try:
        soup = getSoup(searchURL)

        if searchEngine == 'Bloomberg':

            links = []
            for results in soup.find_all('a', href=re.compile('article')):
                if results['href'] not in links:
                    links.append((results['href']))
            
            print ('\nBLOOMBERG RESULTS')
            bloomberg_list_of_results = []
            for link in links:
                
                print (link)
                results_dict =  scrapeWebsite(keyword_list , link)
                bloomberg_list_of_results.append([results_dict,link])
             

            return bloomberg_list_of_results 

        if searchEngine == 'Reuters':

            reuterURLstart= 'https://uk.reuters.com'

            links = []
            for results in soup.find_all('a', href=re.compile('/article')):
                if reuterURLstart+results['href'] not in links:
                    links.append((reuterURLstart+results['href']))

            reuters_list_of_results = []
            print ('\nREUTERS RESULTS')
            for link in links:
                print (link)
                results_dict =  scrapeWebsite(keyword_list , link)
                reuters_list_of_results.append([results_dict,link])
             

            return reuters_list_of_results 
                
                

    except requests.exceptions.RequestException as err:
        print(err)
        pass

def Score(global_rank, bloomberg_results, reuters_results):
    rank_score = 0
    if global_rank > 20000:
        rank_score = 3
    if global_rank > 15000 & global_rank < 20000:
        rank_score = 7
    if global_rank > 10000 & global_rank < 15000:
        rank_score = 12
    if global_rank > 5000 & global_rank < 10000:
        rank_score = 17
    if global_rank > 2500 & global_rank < 5000:
        rank_score = 21
    if global_rank > 1000 & global_rank < 2500:
        rank_score = 25
    if global_rank < 1000:
        rank_score = 30

    bloomberg_resultslength = len(bloomberg_results)
    reuters_resultslength = len(reuters_results)

    result_count = bloomberg_resultslength + reuters_resultslength
    score = 0
    if result_count > 0 & result_count <= 2:
        score = 40
    if result_count > 2 & result_count <= 4:
        score = 48.33
    if result_count > 4 & result_count <= 6:
        score = 53.77
    if result_count > 6 & result_count <= 8:
        score = 58
    if result_count > 8 & result_count <= 10:
        score = 61.96
    if result_count > 11:
        score = 65

    total_score = (rank_score + score)

    return total_score



if __name__ == '__main__':
    
    '''
    submitted_keywords = input('Please provide between 5 and 10 keywords, \n'+
                                'each key word must be greater than 1 character\n'+
                                'and separated by a comma\n')

    submitted_url = input('Please submit url\n')
    '''

    submitted_keywords = 'santa, shooting, pakistan, victims, Texas'
    submitted_url = 'http://www.bbc.co.uk/news/world-us-canada-44179973'
    results = getAlexaResults(submitted_url)
    global_rank = results[0][1]


    submitted_keywords_profiled = profileKeywords(submitted_keywords)

    is_valid_keywords = validKeywords(submitted_keywords_profiled)

    is_url_exists = urlexists(submitted_url)

    if is_valid_keywords and is_url_exists:
        print ('\nURL SUBMISSION RESULTS')
        scrapeWebsite(submitted_keywords_profiled,submitted_url)
        print ('\nALEXA SUBMISSION RESULTS')        
        print(getAlexaResults(submitted_url))
        bloomberg_search = webSearch('Bloomberg',submitted_keywords_profiled)
        reuters_search = webSearch('Reuters',submitted_keywords_profiled)


