# webScraper
Created a web scraper in order to scrape the data from our supplier's website.

I used Pandas to read an excel file which will user provide.
First, I manage the login process using Selenium.
Then, using each product stock code our script will be searching on the website just like a real time user. 
When our bot reaches the product page, the page will be turned into a soup object and then extract the information whichever user wants so. 
After each extraction process, the data which was extracted will be written to the output excel file immediately.
Finally, our code will generate an excel .xlsx file containing the intended data.
