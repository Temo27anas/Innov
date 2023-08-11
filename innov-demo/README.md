# Is Inno Application Demo  
## 1. Introduction
This is a demo for Inno Application. This App is built using Streamlit and based on the Is Inno API
## 2. How to use
### 2.1. Install
To test it localy you can: 
- Clone the repository
- Create a virtual environment
```
python -m venv venv
```
- Activate the virtual environment
```
venv\Scripts\activate
```
- Install the requirements
```
pip install -r requirements.txt
```
- Run the application
```
cd app
streamlit run streamlit_app.py
```
### 2.2. Use
- input the desired website url
- select the desired number of pages to crawl (default is 20)
- click the button
- wait for the result
## 3. Result
The result is a is presented as a notification that shows if the website is innovative or not, along with the score of the whole website. The two tables below show the score of each sentence along with the sentence itself and the url of the page it was found on, for both top positive and top negative sentences.








