
from time import time
from nltk.tokenize import sent_tokenize

from crawling import retrieve_all_text
from keywords import keywords_in_link_to_remove,keywords_in_link_to_check_in
from data_preprocessing import get_website_text
import semantic_search_performer
from os import environ
import mlflow.pytorch


#loading model from mlflow
mlflow.set_tracking_uri(environ.get('TRACKING_URI'))
model = mlflow.pytorch.load_model(environ.get('ISINNO_CLASSIFIER_URI'))
            
            
def predict_sents(sentences, model = model):
    """
    This function returns predictions of a given group of sentences.
    sentences: list of sentences and their links [{"url":url, "sentence":sentence}, ...]
    model: the classifier we use to classify the sentences.

    preds: returns for each sentence investing in innov. and  doing innov. probabilities, innovation negative sentences probability,and
             probability of being irrelevant .
    """
    irr_preds = []
    neg_preds = []
    doing_preds = []
    invest_preds = []
    
    sents = []
    for sent in sentences:
        sents.append(sent)
        sent_predictions = model.predict_proba([sent])[0]
        irr_preds.append(sent_predictions[0])
        neg_preds.append(sent_predictions[1])
        doing_preds.append(sent_predictions[2])
        invest_preds.append(sent_predictions[3])
    return invest_preds, doing_preds, neg_preds, irr_preds

def crawling_website(max_page_number_crawl, website:str, lang="spanish") -> str:
    """"
    this function crawles the content of a website (if possible) and then cut it to chunks, it returns a list of chunks.
    max_page_number_crawl: number of pages to crawl
    website: website address 
    lang: language of the website

    all_texts: list of chunks [{"url":url, "sentence":sentence}, ...]
    """
    _ , html_list = retrieve_all_text(url=str(website), keywords_in_link_to_keep=keywords_in_link_to_check_in, keywords_in_link_to_remove=keywords_in_link_to_remove, max_page_number=max_page_number_crawl)
    
    #get the text of each page  along with its url
    webtext_list = []
    for html in html_list:
        webtext_list.append({"url":html[0], "page_content":get_website_text(html[1])})
    
    #for each page, split the text into sentences
    texts_list = []
    for webtext in webtext_list:
        texts_list.append({"url":webtext["url"], "document":sent_tokenize(webtext["page_content"].replace('\n','.'),language=lang)})
   
   #for each sentence, add the url
    all_texts = []
    for text in texts_list:
        for sentence in text["document"]:
            all_texts.append({"url":text["url"], "sentence":sentence})
    
    #Remove duplicates sentences
    all_texts = list({v['sentence']:v for v in all_texts}.values())

    return all_texts

def get_inno_score(all_texts, number_top_sentences) -> float:
    """
    This function returns the innovation score of a website.
    all_texts: list of chunks [{"url":url, "sentence":sentence}, ...]
    website: website address
    number_top_sentences: number of top sentences to consider
    return: list of tuples (score, link, sentence) [(score, link, sentence), ...]
    """
    if len(all_texts) > 0:
        try:
            #Perform semantic search
            similarties, sentences = semantic_search_performer.semantic_search(all_texts)
            #Getting top n sentencesent
            top_sents, top_links ,top_sims = semantic_search_performer.get_top_sentences(all_texts, similarties= similarties,sentences=sentences,n=number_top_sentences)
        except:
            #If semantic search fails
            return -3
        if len(top_sents) > 0:
            #Predecting the scores of the top sentences
            invest_preds, doing_preds, neg_preds, irr_preds = predict_sents(top_sents, model=model)
            return zip(invest_preds, doing_preds, neg_preds, irr_preds, top_links, top_sents)
        else:
            #If no relevant sentences were found
            return -1

    

def score_websites(website, model = model, nb_page_to_crawl =20, nb_top_sentences = 10, lang="spanish"):
    """
    This function is used to provide the innovation score for a website,
    and gathers all the previous functions. Use this function to get the innovation score of a website.

    website: website address
    Model: the classifier we use to classify the sentences of a website.
    nb_page_to_crawl: number of pages to crawl 
    text_splitter: the method we use to split the text of the website
    nb_top_sentences: number of top sentences to consider
    lang: language of the website

    return: a list of dictionnaries, beach dictionary contains the positive and negative scores, the link and the sentence.

    """
    #start the timer
    start_time = time()
    print("evaluating the website", website)

    #crawling the website 
    all_texts = crawling_website(website=website, max_page_number_crawl=nb_page_to_crawl, lang=lang)
    if len(all_texts) == 0:
        #If No text has been crawled
        return -2
    
    else:         
        scores_website_list = get_inno_score(all_texts, number_top_sentences=nb_top_sentences)
        if scores_website_list == -1:
            return -1
        elif scores_website_list == -3:
            return -3
        else:
            scores_website_list = list(scores_website_list)
            scores_website_list.sort(key=lambda x: x[0], reverse=True)
            scores_dict = [{"invest_score":output[0],
                            "doing_score":output[1],
                            "neg_score":output[2],
                            "irr_score":output[3],
                            "link":output[4],
                            "sentence":output[5]} for output in scores_website_list]
            #stop and print the time
            print("time elapsed: ", time() - start_time)
            return scores_dict
    

