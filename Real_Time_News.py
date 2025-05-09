#Imports
import time
import pandas as pd
from datetime import datetime as d
from Finbert_Utils import estimate_sentiment
from bs4 import BeautifulSoup
import requests
from colorama import Fore, Style


class Analyse_News():

    #Here comes the sentiment analysis
    def inner_loop(self): # We are not using the first source anymore


        """""
        - Scrapt Data from Benzinga.com, Investing.com, Ft.com and Calculate the EMA in Real Time
        - Estimate Sentiment, Positive or Negative
        - Estimate Probatility, up to 1.0
        - Return Sentiment and Probability with Print Statements
        """""

        #Define our current minute
        now = d.now()

        # DEFINE HEADERS SO PEOPLE WON'T BAN OUR IP ADDRESS
        headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Accept-Encoding': 'gzip, deflate, br', 
            'Accept-Language': 'en-US,en;q=0.9',
            'Pragma': 'no-cache' }
        
        """ 
        Function to return probability sentiment
        And a Data Frame with Time, Title and Content
        Of news. This can be applied to any website 
        With similar structure (Block for news, title and content) 
        """
        def get_news(url, headers, table, items, div_1, div_2, title, content):
            try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                news_section = soup.find(div_1, class_=table)
                articles = []
                if not news_section:
                    news_section = f"There's not news for this {url}"
                    return news_section, f"No news section found in {url}"
                news = news_section.find_all(div_2, class_=items)
                for i in news:
                    try:
                        article_title = i.find(class_=title)
                        article_content = i.find(class_=content)
                        title_text = article_title.get_text(strip=True) if article_title else "No title found"
                        content_text = article_content.get_text(strip=True) if article_content else "No content found"
                        if article_title and not article_content:
                            print(f"No Title or Content {url}")
                            # Scraping the entire news_section or a specific part of it
                            section_text = news_section.get_text(strip=True) if news_section else "No valid section found"
                            articles.append({
                                "Time": now,
                                "Title": "No title found",
                                "Content": section_text
                            })
                        else:
                            articles.append({
                                "Time": now,
                                "Title": title_text,
                                "Content": content_text
                            })
                    except Exception as e:
                        # Log error for each individual article
                        print(f"Error extracting data for one article: {str(e)}")
                        # You can choose to append a placeholder or skip the article
                        articles.append({
                            "Time": now,
                            "Title": "Error scraping title",
                            "Content": "Error scraping content"
                        })   
                if not articles:
                    # Scraping the entire news_section or a specific part of it
                    section_text = news_section.get_text(strip=True) if news_section else "No valid section found"
                    articles.append({
                        "Time": now,
                        "Title": "No title found",
                        "Content": section_text
                    })
                full_news = pd.DataFrame(articles)
                articles_full = full_news.to_string(index=False)
                probability, sentiment = estimate_sentiment(news=articles_full)
                return probability, sentiment, full_news
            except Exception as e:
                return None, f"Error scraping {url}: {str(e)}"

        #YOU MAY TRY BLOOMBERT IF DESIRED
        # # First SOURCE BLOOMBERG
        # url_1 = "https://www.bloomberg.com/search?query=XAU"
        # headers = headers
        # table_1 = "contentWell__8c4b2fab1e withLightBorder__2c4cfe002c"
        # items_1 = "text__47d6cb9756 withThumbnail__547a423017"
        # div_1_1 = 'div'
        # div_2_1 = 'div'
        # title_1 = "headline__3a97424275"
        # content_1 = "summary__a759320e4a"
        # probability_1, sentiment_1 = get_news(url=url_1, headers=headers, table=table_1, items=items_1, div_1=div_1_1, 
        #                                       div_2=div_2_1, title=title_1, content=content_1)
        #SECOND SOURCE BENZINGA
        url_2 = "https://www.benzinga.com/search?q=XAU+USD"
        table_2 = "content-feed-list"
        items_2 = 'list-item-title'
        div_1_2 = 'div'
        div_2_2 = 'a'
        title_2 = None
        content_2 = None
        probability_2, sentiment_2, articles_full_2 = get_news(url=url_2, headers=headers, table=table_2, items=items_2, div_1=div_1_2, 
                                                div_2=div_2_2, title=title_2, content=content_2)

        #THIRD SOURCE INVESTING.
        url_3 = "https://www.investing.com/currencies/xau-usd-news"
        table_3 = "mb-4"
        items_3 = "flex py-6 sm:flex-row-reverse md:flex-row"
        div_1_3 = 'div'
        div_2_3 = 'article'
        title_3 = 'block text-base font-bold leading-5 hover:underline sm:text-base sm:leading-6 md:text-lg md:leading-7'
        content_3 = 'mt-2 hidden text-xs leading-5 text-[#5B616E] md:block'
        probability_3, sentiment_3, articles_full_3 = get_news(url=url_3, headers=headers, table=table_3, items=items_3, div_1=div_1_3, 
                                                div_2=div_2_3, title=title_3, content=content_3)


        # #FOURTH RESOURCE ---GENERAL ECONOMIC NEWS---
        url_4 = "https://www.ft.com/us-dollar"
        table_4 = "o-teaser-collection__list js-stream-list"
        items_4 = "o-teaser-collection__item o-grid-row"
        div_1_4 = 'ul'
        div_2_4 = 'li'
        title_4 = 'js-teaser-heading-link'
        content_4 = 'js-teaser-standfirst-link'
        probability_4, sentiment_4, articles_full_4 = get_news(url=url_4, headers=headers, table=table_4, items=items_4, div_1=div_1_4, 
                                        div_2=div_2_4, title=title_4, content=content_4)
        
        #Gold Goes up when the market sentiment is negative
        #Rest the probability to showcase this negative correlation
        r = 1.25 - probability_4 # r because I wish :)
        
        #The same applies for the sentiment
        def usd_dollar(sentiment_4):
            if sentiment_4 == 'positive':
                    sentiment_4 = 'negative'
            elif sentiment_4 == 'negative':
                sentiment_4 = 'positive'
            else:
                sentiment_4 = 'neutral'
            return sentiment_4
        
        #Get last sentiment
        usd_sentiment = usd_dollar(sentiment_4)

        #Take Average Sentiment
        sentiments = [ sentiment_2, sentiment_3, usd_sentiment]
        sentiment_values = {"positive": 1, "neutral": 0, "negative": -1}
        numerical_sentiments = [sentiment_values[sentiment] for sentiment in sentiments]
        average_sentiment = sum(numerical_sentiments) / len(numerical_sentiments)
        if average_sentiment > 0:
            overall_sentiment = "positive"
        elif average_sentiment < 0:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"   

        average = [probability_2, probability_3, r]
        
        #YOU CAN ADD WITHTS TO THE NEWS PROBABILITIES
        weights = [1, 1, 1]
        weighted_sum = sum(p * w for p, w in zip(average, weights))

        #Take the Average Probability
        average_probability = weighted_sum / len(average)

        #PRINT WHAT"S HAPPENING
        print(Fore.MAGENTA + f"Time {now} Average Probability: {average_probability} Overall Sentiment: {overall_sentiment}")
        print(Style.RESET_ALL)

        """
        Prints
        """
        print(Fore.BLUE, "Probability 1:", probability_2)
        print("Probability 2:", probability_3)
        print("Probabitlity 3:", r)
        print("Sentiment 1:", sentiment_2)
        print("Sentiment 2:", sentiment_3)
        print("Sentiment 3:", usd_sentiment) 
        print(Style.RESET_ALL)

        return articles_full_2, articles_full_3, articles_full_4, probability_2, probability_3, r, sentiment_2, sentiment_3, usd_sentiment
    
    def outer_loop(self):
        """
        Outer Loop
        -Get the Sentiments and Probabilities to Invest
        -Get a Temporal dataframe to determinate when to close orders
        -Scrapt prices for Positional Sizing if the market is closed
        -Use the Predicted Df with a Slice of Data to invest in the lowest price and sell in the highest
        -Define Buy, Sell and Close orders
        -Define Limits
        -Use the Logic implemented to run each minute and invest
        """
        #Initialize our start time
        start_time = time.time()

        #average_probability, overall_sentiment, 
        articles_full_2, articles_full_3, articles_full_4, probability_2, probability_3, r, sentiment_2, sentiment_3, usd_sentiment = self.inner_loop()

        seconds = 900 #Secons to run again

        while True:

            if time.time() - start_time >= seconds: #GET THE NEWS EACH *15* MINUTES // YOU CAN CHANGE IT IF YOU WISH
                
                articles_full_2, articles_full_3, articles_full_4, probability_2, probability_3, r, sentiment_2, sentiment_3, usd_sentiment = self.inner_loop()

                if articles_full_2.empty and sentiment_2 == None:
                    
                    print(Fore.RED +"We Don't have the sentiment and probability to invest")
                    print(Fore.RESET)
                    continue


                articles_full_2['Probability'] = probability_2
                articles_full_3['Probability'] = probability_3
                articles_full_4['Probability'] = r

                articles_full_2['Sentiment'] = sentiment_2
                articles_full_3['Sentiment'] = sentiment_3
                articles_full_4['Sentiment'] = usd_sentiment


                news_df = pd.concat([articles_full_2, articles_full_3, articles_full_4], ignore_index=True)
                
                #You can drop the duplicated rows
                news_df = news_df.drop_duplicates()

                """  
                This will automatically generate a df
                with the news you want to get each m seconds
                """
                #Save to a DataFrame is Updated every M Minutes
                news_df.to_csv("Financial_Data.csv", mode="a", header=False, index=False)

                print(f"Running each {seconds/60} minutes")

                start_time = time.time()
    
#RUN IN CONSOLE
if __name__ in "__main__":

    on = Analyse_News()
    
    try: 
        on.outer_loop()

    except KeyboardInterrupt: #Automatic interruption with control + C
        print("Interrupted by user")