# FinBERT: Real-Time Financial News Sentiment Analysis

## Overview
This repository teaches you how to scrape real-time financial news from **ANY** website and extract key insights, including **title, content, sentiment probability, and overall sentiment classification**.

We utilize **FinBERT**, a specialized fine-tuned BERT model designed for financial data analysis. Unlike general NLP models, FinBERT excels in extracting and analyzing financial sentiment with greater accuracy.

## Websites
This implementation demonstrates sentiment analysis for financial news scraped from the following sources:
- [Benzinga](https://www.benzinga.com) (XAU/USD news)
- [Investing](https://www.investing.com) (XAU/USD news)
- [Financial Times](https://www.ft.com) (General market news)
- Any other website with the following structure: (News Block, Title and Content of news)

## Purpose
The goal of this repository is to **teach users how to scrape, analyze, and store financial news in a structured DataFrame** for further use. You can apply these techniques to ANY website, as long as they provide a clear news block with titles and contents.

For this experiment, we chose to analyze XAU/USD (Gold vs USD) market news—because, let's be honest, **gold is shiny and who doesn’t like shiny?** ✨

## How It Works
By running the `Real_Time_News.py` script, you'll automatically:
1. Scrape financial news in **real-time**.
2. Perform sentiment analysis using **FinBERT**.
3. Generate and update a `.csv` file containing:
   - **Title** of the news
   - **Content** of the article
   - **Sentiment probability scores**
   - **Overall sentiment classification (Positive, Neutral, Negative)**

This ensures you always have the **latest financial insights** without lifting a finger—just press **Run**, and let automation handle the rest! 

## Ready to Start? 🚀
If you're eager to **automate financial news analysis**, this repository is your gateway to hands-free data collection and sentiment estimation.

Let's get started! **(⌐■_■)**
