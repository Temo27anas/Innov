import pandas as pd
from  requests import post
import streamlit as st
from os import environ
import json


def get_process_sentences(website, nb_page_to_crawl, nb_output_sentences, nb_top_invest_sentences, nb_top_doing_sentences, nb_top_neg_sentences, nb_top_irr_sentences):

    """
    This function calls the API to get the sentences and their innovation scoring.
    Then it processes the results to get the top sentences of each class
    Input: website: the website to crawl,
        nb_page_to_crawl: the number of pages to crawl,
        nb_output_sentences: the number of sentences to return,
        nb_top_invest_sentences: the number of top sentences to return for the invest class,
        nb_top_doing_sentences: the number of top sentences to return for the doing class,
        nb_top_neg_sentences: the number of top sentences to return for the negative class,
        nb_top_irr_sentences: the number of top sentences to return for the irrelevant class

    Output: max_score_invest: the max score for the invest class,
            max_score_doing: the max score for the doing class,
            df_invest: dataframe of the top sentences for the invest class,
            df_doing: dataframe of the top sentences for the doing class,
            df_neg: dataframe of the top sentences for the negative class,
            df_irr: dataframe of the top sentences for the irrelevant class
            OR None if there is an error OR No relevant sentences found

    """
    #send request to API
    payload = {"url":website, "nb_page_to_crawl":nb_page_to_crawl, "nb_output_sentences": nb_output_sentences}
    response = post(environ.get('CALLBACK_URL', "http://127.0.0.1:5607")
                    , json=payload, timeout=400)
    
    #if request is successful
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df = df[["sentence", "invest_score", "doing_score", "neg_score" , "irr_score", "link"]]
        links = df["link"].unique()
        max_score_invest= df['invest_score'].max()
        max_score_doing= df['doing_score'].max()
        
        #get top sentences following each class, if any, and sort them by score. The sentences must have a score > 0.5 to be considered
        df_invest = df[df["invest_score"] > 0.5].sort_values(by="invest_score", ascending=False).head(nb_top_invest_sentences)
        df_doing = df[df["doing_score"] > 0.5].sort_values(by="doing_score", ascending=False).head(nb_top_doing_sentences)
        df_neg = df[df["neg_score"] > 0.5].sort_values(by="neg_score", ascending=False).head(nb_top_neg_sentences)
        df_irr = df[df["irr_score"] > 0.5].sort_values(by="irr_score", ascending=False).head(nb_top_irr_sentences)


        return links, max_score_invest,max_score_doing, df_invest, df_doing, df_neg, df_irr
    
    #No crawled text found
    elif response.status_code == 290:
        st.write("No crawled text found. Please check this website or try another one")
        return None, None, None, None, None, None, None
    
    #No relevant sentences found
    elif response.status_code == 291:
        st.error("This website is not innovative! No relevant sentences found.", icon="❌")  
        return None, None, None, None, None, None, None
    #Genaeral error format
    else:
        st.error(f'Error: {response.json()["detail"]}. Please check your URL or your internet connection')
        return None, None, None, None, None, None, None

        


