from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate 
from falsifier.forms import SearchCriteriaForm , SignUpForm
from falsifier.models import  Search , SearchKeywordResults , SearchResults , AlexaResults
from falsifier.scripts import *

# Create your views here.


class index(generic.ListView, FormView):
    

    def get(self,request):
        template_name = 'falsifier/index.html'

        return render(request, template_name)
    
class search(generic.ListView, FormView):


    #context_object_name = 'service_type'
    def get(self,request):
        template_name = 'falsifier/search.html'
        form = SearchCriteriaForm()
        if request.user.is_authenticated:
            return render(request, template_name, {'form':form})
        else:
            return redirect ('/falsifier/login/')

    def post(self,request):
        

        template_name = 'falsifier/search.html'
                        
        form = SearchCriteriaForm()
        if request.user.is_authenticated:
            
            form = SearchCriteriaForm(request.POST or None)
            if form.is_valid():
                listofkeywords = form.cleaned_data['listofkeywords']
                searchURL = form.cleaned_data['searchURL']
                
                valid = False
                if listofkeywords != '' and searchURL != '':
                        #Call Validation methods to validate the minimum 5 key words,
                    submitted_keywords = listofkeywords
                    submitted_keywords_profiled, count_of_keywords = profileKeywords(submitted_keywords)            #and the URL depending on validation set valid to true or false
                    if count_of_keywords >= 5 and count_of_keywords <= 10:
                        valid = True
                    else:
                        invalid_keywords = 'Please input a minimum of 5 keywords'
                        check_keywords = invalid_keywords
                        return render(request, template_name, {'form':form, 'check_keywords': check_keywords })
                    
                    submitted_url = searchURL                    
                    is_url_exists = urlexists(submitted_url)
                    
                    if is_url_exists:
                        valid = True
                    else:
                        invalid_url = 'Please input a valid URL'
                        invalid_url = invalid_url
                        return render(request, template_name, {'form':form, 'invalid_url': invalid_url })                        
                        
                    if valid:
                                    #Call main functions URL, Reputable sources etc

                                    #Create object to store output from Results
                                    #outputResults = Results

                        

                        is_valid_keywords = validKeywords(submitted_keywords_profiled)

                        

                        if is_valid_keywords and is_url_exists:
                        
                            sc = Search()
                            sc.listofkeywords = listofkeywords
                            sc.submittedURL = searchURL
                            sc.isCurrentSearch = True
                            sc.user = request.user
                            sc.save() 


                            print ('\nURL SUBMISSION RESULTS')
                            submission_results = scrapeWebsite(submitted_keywords_profiled,submitted_url)
                            print (submission_results)
                            sr = SearchResults()
                            sr.sumOfKeywords = submission_results['sumOfWordCount']
                            sr.keywordOccurence = submission_results['occurrence_percent']
                            sr.totalWordCount = submission_results['totalWordCount']
                            sr.search = sc
                            sr.save()

                            #Store keyword results
                            #
                            for x, a in enumerate(submission_results['keyword_match_results']):
                                skr = SearchKeywordResults()
                                skr.keywordCount = submission_results['keyword_match_results'][x][1]
                                skr.keyword = submission_results['keyword_match_results'][x][0]
                                skr.search = sc
                                skr.save()

                            print ('\nALEXA SUBMISSION RESULTS')        
                            alexa_results = getAlexaResults(submitted_url)
                            ar = AlexaResults()
                            for x,a in enumerate(alexa_results):
                                ar.search = sc
                                if alexa_results[x][0] == 'Global Rank':
                                    ar.globalRank = alexa_results[x][1]
                                if alexa_results[x][0] == 'Country Rank':
                                    ar.countryRank = alexa_results[x][1]
                                if alexa_results[x][0] == 'Bounce Rate':
                                    ar.BounceRate = float(alexa_results[x][1] .replace('%',''))                                                                       
                                if alexa_results[x][0] == 'Daily Page Views':
                                    ar.DailyPageViews = alexa_results[x][1]
                                if alexa_results[x][0] == 'Daily Time Spent':
                                    ar.DailyTimeSpent = alexa_results[x][1]
                                if alexa_results[x][0] == 'Search Visits':
                                        ar.SearchVisits = float(alexa_results[x][1].replace('%',''))

                            ar.save()

                            print('\nSEARCH ENGINE RESULTS')
                            bloomberg_results = webSearch('Bloomberg',submitted_keywords_profiled)
                            bloomberg_numberofresults = len(bloomberg_results)
                            reuters_results =  webSearch('Reuters',submitted_keywords_profiled)
                            reuters_numberofresults = len(reuters_results)




                            # print ('reuters print')
                            # print ('\n')
                            # print (reuters_results[0][0]['totalWordCount'])
                            # print (reuters_results[0][1])
                            # print (reuters_results[1][1])
                            # print (len(reuters_results))
                            # print('SSSSSSSSSSS')


                            for    index, rr in enumerate(reuters_results):
                                print (index)
                                for n, a in enumerate(rr):
                                    print(n , " inside")
                                    print (a)


                            '''
                            search = Search()
                            search.listofkeywords = submitted_keywords
                            search.submittedURL = submitted_url
                            search.save()
                            
                            search_results = SearchResults()
                            search_results.search = search
                            search_results.totalWordCount = submission_results.totalWordCount
                            search_results.sumOfKeywords = submission_results.sumOfWordCount
                            search_results.keywordOccurence = submission_results.occurrence_percent
                            search_results.save()
                            '''


                            for col in submission_results['keyword_match_results']:
                                keyword , cnt = col

                                print (keyword , cnt)
                            
                        result = Score(ar.globalRank, bloomberg_results, reuters_results)
                        print("Falsifier Score:", result)
                        #update historic records in Search Criteria with false in the isCurrentSearch

                        #return render(request, template_name , {'outputResults':outputResults})
                        Results = "Fake News" #Dummy Results
                        outputResults = Results

                        return render(request, template_name,{'form':form , 'submission_results': submission_results, 
                        'alexa' : alexa_results, 'submission_url':submitted_url, 'bloomberg_results':bloomberg_results,
                        'reuters_results': reuters_results})
                    #else:
                        #This is when URL link is broken OR user supplied incorrect number of keywords
                        #return render(request, template_name, {'form':form})          
                else:
                    searchInputInvalid = 'Invalid Search Input'
                    searchCriteriaFormInput = searchInputInvalid
                    return render(request, template_name, {'form':form, 'searchCriteriaFormInput': searchCriteriaFormInput})                                         
                     
            else:

                return render(request, template_name, {'form':form}) 
        else:
            return redirect('/falsifier/' )

        


class history(generic.ListView, FormView):
    

    def get(self,request):
        template_name = 'falsifier/history.html'
        form = SearchCriteriaForm()
        if request.user.is_authenticated:
            return render(request, template_name)
        else:
            return redirect ('/falsifier/login/')



class signup(generic.ListView,FormView):

    def get (self, request):
         
        template_name = 'registration/signup.html'
        form = SignUpForm()

        return render(request, template_name,{'form':form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/falsifier/user_homepage')
        else:
            template_name = 'registration/signup.html'
            form = SignUpForm()
            return render(request, template_name,{'form':form})

class user_homepage(generic.ListView, FormView):
    def get(self, request):
        template_name = 'falsifier/user_homepage.html'
        return render (request, template_name)

                    
