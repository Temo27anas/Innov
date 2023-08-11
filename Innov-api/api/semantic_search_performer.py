#Sentence transformer
import faiss
from numpy.linalg import norm
from numpy import asarray
from numpy import where
import requests
from os import environ
from config import VEC_DB_FILE_NAME

# Deserialize the index from a file
index = faiss.read_index(f"vector_databases/{VEC_DB_FILE_NAME}")


def get_normalized_embeddings(all_texts:list):
    """
    This function is only used to normalize the embeddings in order to calculate the cosine similarity.
    sentences:
    all_texts: list of chunks [{"url":url, "sentence":sentence}, ...]

    returns: list of normalized embeddings
    """
    sentences = [text["sentence"] for text in all_texts]
    inputs = {"text" : sentences} 
    URL = environ.get('URL_TEXT_EMBEDDING')
    res = requests.post(url = URL, json = inputs)  
    sentence_embeddings = res.json()['embeddings'] 
    norm_embds = [vector/norm(vector) for vector in sentence_embeddings]
    return asarray(norm_embds)


def semantic_search(docs:list, k : int = 1):

    """
    This function returns the similarties between the website chunks and the relvent sentences from the vector database
    
    docs: list of chuncks (all_texts): [{"url":url, "sentence":sentence}, ...]
    k : number of similar sentences to retrieve for each chunk
    sentence_transformer :  the embedding method (should be the same as the one used to embedd the sentences in th VB)
    """

    embeddings = get_normalized_embeddings(docs)
    res = index.search(embeddings, k)
    return res[0], docs


def get_top_sentences(all_texts, similarties : list, sentences :list, n:int, threshold:float = 0.70) -> list:
    """
        This function returns the top_n similar chunks to our relvent sentences 
        similarties : list of similarties (by semantic search)
        sentences : list of sentences (from the website)
        n : number of sentences to consider
        thereshod:
    """
    sorted_sim = sorted(similarties, reverse=True)
    top_n = [sim for sim in sorted_sim[:n] if sim > threshold]
    indexes = [where((similarties == sim))[0][0] for sim in top_n]
    top_sents = [all_texts[i]["sentence"]   for i in indexes]
    top_links = [all_texts[i]["url"] for i in indexes]
    return top_sents, top_links, top_n
