import pandas as pd
from  requests import post
import streamlit as st
from os import environ


def get_process_sentences(website, nb_page_to_crawl =20, nb_output_sentences=20):
    """


    """

    payload = {"url":website, "nb_page_to_crawl":nb_page_to_crawl, "nb_output_sentences": nb_output_sentences}
    response = post(environ.get('CALLBACK_URL')
                   , json=payload, timeout=400)
       

    if response.status_code == 200:  
        df = pd.DataFrame(response.json())
        df = df[["sentence", "invest_score", "doing_score", "neg_score" , "irr_score", "link"]]
        max_score_invest= df['invest_score'].max()
        max_score_doing= df['doing_score'].max()
        inno_score = max(max_score_invest, max_score_doing)

        if len(df['invest_score']) == 0 and len(df['doing_score']) == 0:
            return -1 #NotInno
        elif inno_score > 0.5 :
            if inno_score == max_score_doing: #Doing
                return 1
            elif inno_score == max_score_invest:
                return 2 #Invest
            else:
                return 3 #Both
        else:
            return -1 #NotInno

    elif response.status_code == 290:
        return -2 #Fail
    
    #No relevant sentences found
    elif response.status_code == 291:
        return -1 #NotInno
    
    #Genaeral error 
    else:
        return -2 #Fail

        


