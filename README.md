# Falsifier
This project is a web application made using the Django Framework. This application was created as a solution to the widespread issue
of fake news and its purpose is to evaluate the truth of a web article less than 24 hours old by cross-referencing searches among two trusted 
news sources.

The project is designed to take a link to a webpage (preferably an article) and five descriptive key words as input:

1) Visit the link and copy the entire article for analysis. The analysis consists of finding the 10 most frequent key words, 
which are pasted into both reuters and bloomberg news search engines in addition to those initially provided, the search is set 
within a 24 hour period. I have engineered a score system which scores based on the number of relative links returned from both 
search engines

2) The link is also pasted into alexa, a page ranking website for which I have engineered a score system based on the sites popularity
where high-ranking sites are frequently visited hence are far less likely to publish fake news articles.

3) Both search engine and alexa scores are added together giving the final score.

