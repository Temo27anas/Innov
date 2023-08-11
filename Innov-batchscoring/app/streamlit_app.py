import streamlit as st
import pandas as pd
import time
from config import THREADS_NUM
from import_data import get_process_sentences
from multiprocessing.pool import ThreadPool
import bcrypt
from os import environ


def app():
        
    uploaded_file = st.file_uploader("1- Upload a csv file 📄")

    #check if file is uploaded
    if uploaded_file is not None:
        #check if file is csv
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            with st.expander(f"Show Websites :" ):
                st.write(df)
        else:
            st.warning("Please upload a csv file")
            st.stop()

        #check if file has the right column name and is not empty and has only one column 
        if 'website' in df.columns and len(df) > 0 and len(df.columns) == 1:
            st.success("File uploaded successfully")
        else:
            st.warning("Please make sure your file has a column named 'website'")
            st.stop()

        #Evaluation section
        if st.button('2- Evaluate Innovation 🚀'):
            try: 
                with st.spinner(f'Getting innovation score...'):
                    
                    pool = ThreadPool(THREADS_NUM)
                    results = pool.map(get_process_sentences, df['website'].tolist())
                    pool.close()
            except:
                st.error("Error: Couldn't get the scorings")
                st.stop()

            #print a summary of the results
            df['innovation_score'] = results
            df['innovation_score'] = df['innovation_score'].replace({-1:'NotInno', 1:'Doing', 2:'Invest', 3:'Both', -2:'Fail'})
            st.write(df)
        



if 'is_logged' not in st.session_state:
    st.session_state.is_logged = False

st.set_page_config(page_title='IsInno Batch Scoring App', layout='wide')
st.title('💯 IsInno Batch Scoring App')
with st.sidebar:

    st.image("./assets/logo_leyton.png", width=300)
    st.header('IsInno Batch Scoring App:')
    st.write('This app allows you to upload a csv file with a list of websites and get their innovation score.')
    
    # login section
    if st.session_state.is_logged:
        st.success('Authentication successful')
      
    else:
        st.header('Login:')
        st.write('Please enter the key to access the app:')
        input_key = st.text_input('Key', type='password')
        if st.button("Login"):
            if bcrypt.checkpw(input_key.encode('utf-8')
                               , environ.get('AUTH_KEY_HASH')):
                st.session_state.is_logged = True
                st.success('Authentication successful')
               
            else:
                st.error('Authentication failed')
                st.stop()


if st.session_state.is_logged:
    app()





    st.markdown("""---""")
    st.write('Version 0.1.0')






                



    