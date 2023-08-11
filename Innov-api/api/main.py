from fastapi import FastAPI, Response
from pydantic import BaseModel
import pipeline
import requests

app = FastAPI(title="IsInno API", description="API to predict innovation based on sentences crawled from a given website url", version="0.1")

class ScoringItem(BaseModel):
    url: str
    nb_page_to_crawl: int
    nb_output_sentences: int

@app.post("/")


async def scoring_endpoint(item: ScoringItem, response: Response):
    try:
        sc1 = pipeline.score_websites(website=item.url, nb_page_to_crawl=item.nb_page_to_crawl, nb_top_sentences=item.nb_output_sentences)
        if sc1 == -2:
            response.status_code = 290
            return {"detail": "NoCrawledTextFound"}
        elif sc1 == -1:
            response.status_code = 291
            return {"detail": "NoRelevantSentsFound"}
            
        elif sc1 == -3:
            response.status_code = 490
            return {"detail": "CannotPerformSemanticSearch"} 
                   
        else:
            return sc1
            
    except requests.exceptions.ConnectionError as e:
        response.status_code = 491
        return {"detail": "ConnectionError"}
    
    except requests.exceptions.InvalidURL as e:
        response.status_code = 492
        return {"detail": "InvalidURL"}
    
    except requests.exceptions.HTTPError as err:
        response.status_code = 493
        return {"detail": "HTTPError"}
    
    except Exception as e:
        if "TimeoutError" in str(e):
            response.status_code = 494
            return {"detail": "TimeoutError"}
        else:
            response.status_code = 495
            print(e)
            return {"detail": "UnknownError"}
    
   

    