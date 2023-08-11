import streamlit as st
from streamlit_modal import Modal
from process_db import insert_sentences

#report popup modal
modal_report = Modal("Thank you!",
                     max_width=300,
                     padding=20,
                    key="modal_report")

def return_key(label_name, i):
    """
    This function returns a unique key for each button
    """

    if label_name == "invest_score":
        label_name = 1000
    elif label_name == "doing_score":
        label_name = 2000
    elif label_name == "neg_score":
        label_name = 3000
    label_name =int(str(label_name) + str(i))
    return label_name


def report_sentences(sentence, hand_label):
    """
    This function saves the reported sentence in a SQL database
    Input: the sentence to report, the hand label
    Output: None
    """
    #insert into DB
    insert_sentences(sentence, hand_label)

    #show the Pop-up after the feedback 
    with modal_report.container():
        st.write("Thank you for your feedback!")
        st.write("We will use your feedback to improve our model.")
                   

def make_clickable(link):
    """
    This function makes a URL clickable
    Input: a URL
    Output: a clickable URL
    """
    text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{text}</a>'


def create_table(df, label_name):   
    """
    Create a table to display the sentences and their innovation scoring
    Input: a pandas dataframe, the scores of a column to display in bold
    Output: a streamlit table with the sentences, URL, and their innovation scoring.
    """
    if len(df) == 0:
        st.write("No sentences found")
    else:
        colms = st.columns((6.5, 2, 2, 2, 2.25, 4.25))
        fields = ["Sentence", "Invest Score", "Doing Score", "Negative Score", "Irrelevant Score", "Go to Link"]
        for col, field in zip(colms, fields):
            col.write(field)

        for i in range(len(df)):
            col1, col2, col3, col4, col5, col6  = st.columns((6.5, 2, 2, 2, 2.25, 4.25))
            #Sentence
            col1.write(df.iloc[i, 0])
            #Scores
            col2.write( (f"**{round(df.iloc[i, 1] * 100 , 2)} %**") if label_name == "invest_score" else f"{round(df.iloc[i, 1] * 100 , 2)} %") #Invest
            col3.write(  (f"**{round(df.iloc[i, 2] * 100 , 2)} %**") if label_name == "doing_score" else f"{round(df.iloc[i, 2] * 100 , 2)} %") #Doing
            col4.write( (f"**{round(df.iloc[i, 3] * 100 , 2)} %**") if label_name == "neg_score" else f"{round(df.iloc[i, 3] * 100 , 2)} %") #Negative
            col5.write(str(round(df.iloc[i, 4] * 100 , 2)) + '%' ) #Irrelevant
            #Link
            col6.write(df.iloc[i, 5])
            #report mispredicted sentences           
            with st.expander("🚩 Report this mispredicted sentence:"):
                col1, col2, col3, col4  = st.columns([1,1,1,1])
                with col1 :
                    report_buy_bu = st.button("💰 Buying", key=f"{return_key(label_name, i)}_buy", on_click=report_sentences, args=(df.iloc[i, 0], "buying"), disabled=(label_name == "invest_score") )
                with col2:
                    report_do_bu = st.button("🛠️ Doing", key=f"{return_key(label_name, i)}_do", on_click=report_sentences, args=(df.iloc[i, 0], "doing"), disabled=(label_name == "doing_score"))
                with col3 :
                    report_neg_bu = st.button("👎 Negative", key=f"{return_key(label_name, i)}_neg", on_click=report_sentences, args=(df.iloc[i, 0], "negative"), disabled=(label_name == "neg_score"))
                with col4:
                    report_irr_bu = st.button("🤷 Irrelevant", key=f"{return_key(label_name, i)}_irr", on_click=report_sentences, args=(df.iloc[i, 0], "irrelevant"), disabled=(label_name == "irr_score"))

              
                