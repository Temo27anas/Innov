# Is Inno API

An API for the detection of Innovation from companies' websites. 
The API can output the innovation scores of a website after crawling it, and extracting the relevant sentences using semantic similarity, and then predicting the scores using a  sentence classification model.
The scores consists of : buying innovation, doing innovation, negative sentences about innovation, and irrelevance scores.
The API outputs the innovation scores, the sentence, and the link to the page where the sentence was found for the top "nb_output_sentences" sentences with the highest "buying innovation" score.
## Running the API

### Installation
- Clone the repository
- To run the API on your local machine, simply run the following commands:
* **Building Docker image**, through the following command:

```bash
docker build -t isinnoapi .
```

* **Running Docker image**, through the following command:

```bash
docker run -d -p 5607:5607 isinnoapi
```

* Finally, navigate to [http://localhost:5607](http://localhost:5607) to view the Swagger UI.

## Using the API

### Endpoints

#### /
- Method: POST
- Description: Returns the innovation score of a given website.
- Body:
```
{
    "url": "https://www.example.com"
    "nb_page_to_crawl": 10,
    "nb_output_sentences": 10
}
```
- Response:
The API outputs following the specified nb_output_sentences; A list of dictionaries with the following keys: Each element in the sub-list is contains several dictionaries with the following keys:
```
[ {
      "invest_score":
      "doing_score": 
      "neg_score": 
      "irr_score": 
      "link":
      "sentence": 
    },

    ...
]
```








