# Team - Project 1 Crypto Sentiment Proposal

### Project Title
    Crypto Trend and Sentiment Analysis

### Team Members
    Bryn Lloyd-Davies
    Matt Newkirk
    Michael Garcia
    Justin Bernier

### Project description / outline
    Relating twitter sentiment analysis to crypto price action and volume

### Research questions to answer
Does Bitcoin lead other crytocurrencies and is there a strong correlation between Bitcoin, Ethereum, and Litecoin?

    Yes, we saw correlation between between Bitcoin and other popular cryptocurrencies.

Is there correlation of big twitter influencers sentiment to crypto price action and volume?
    
    Short answer: maybe. There were points where large shifts in volume traded did correspond to tweets that had been largely interacted with with a polarity rating, but we lacked enough evidence to conclude that the correlation was also causation.


    
Time-analysis of trend and possible social media correlations
     
     Because our crypto data is only by day and not minute by minute, it makes pinpointing immediate effects difficult, and limits us to only correlating large scale spikes. We are also limited by our data in being able to determine outside effect vs tweet effect and baseline movement. 
     
     Someone like Vitali or McAfee tweet very regularly about crypto, so with the data we had it was difficult to determine if a change was just a regular change, or due to their tweet. We are also limited in only being able to analyze the sentiment of the tweet itself, and not the sentiment of the replies to it, which is arguably the bigger indicator in whether people will be choosing to trade based on what the influencer tweeted. 
     
     We were limited to deriving implied impact by multiplying the polarity rating by the favorite count, which scaled the favorites and assigned them a negative or positive rating. Again, this is applying the polarity of the tweet to the interaction which may not be very accurate in terms of determining sentiment of the reception. 


### Datasets to be used
    Coinbase Pro - Daily crpto data
    Twitter API
    TextBlob Library
    Tweepy Library

### Rough breakdown of tasks
    Get crypto data
    Get twitter sentiment data
    Clean up data and filter on crypto of interest
    Visualize data and look for dates of tweets and volume/price action of crypto

### Key Files
    notebooks/final_presentation_notebook.ipynb - notebook used for in class presentation
    notebooks/twitter_reader - the main notebook used to pull twitter API data
    Michael_edits/data_cleaner_main.ipynb  - main notebook useed to pull crypto data and clean it.
    FinTech - Crypto Dashboard.pdf - Presentation Deck
    