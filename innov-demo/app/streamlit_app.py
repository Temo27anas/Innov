import streamlit as st
from import_sentences import get_process_sentences
from os import environ
from table_generator import create_table, make_clickable

#initialize the session state
if "imported_data" not in st.session_state:
    st.session_state["imported_data"] = []


st.set_page_config(page_title='IsInno Demo App 💡', layout='wide')
st.title('IsInno Demo App 💡')

website = st.text_input('🌐 Enter a website URL', placeholder= "Put the URL of a website here!")
nb_page_to_crawl = st.slider('📃 Select the maximum number of pages to crawl:', 0, 100, 20)

with st.sidebar:
    st.image("./assets/logo_leyton.png", width=300)
    st.header('About IsInno:')
    st.write('IsInno is an innovation scoring tool that helps you to assess the innovation level of a company based on its website content.')
    st.markdown("""---""")
    st.write('Version 0.1.0')
    
if st.button('Get Innovation Score 🚀'):
    with st.spinner(f'Getting innovation score for {website}...'): 
        
        # Get processed sentences and innovation scoring
        try:
            st.session_state["imported_data"] = get_process_sentences(website, nb_page_to_crawl, 
                                                                            environ.get('NB_OUTPUT_SENTENCES', 30),
                                                                            environ.get('NB_TOP_INVEST_SENTENCES', 3),
                                                                            environ.get('NB_TOP_DOING_SENTENCES', 3),
                                                                            environ.get('NB_TOP_NEG_SENTENCES', 3),
                                                                            environ.get('NB_TOP_IRR_SENTENCES', 3)
                                                                            )
            
        except Exception as e:
            st.error('User side Error or Couldn\'t make a connection to the server')
            print(e)
            st.stop()

#check if there is data to display
if st.session_state["imported_data"] == []:
    st.stop()

else: 
    links, max_score_invest, max_score_doing, top_sents_invest, top_sents_doing, top_sents_neg, top_sents_irr = st.session_state["imported_data"]
    st.write('Done!')

    # Display the crawled pages in an expander
    with st.expander(f"Show Crawled pages: ({len(links)} pages in total)"):
        for link in links:
            st.write(make_clickable(link), unsafe_allow_html=True)
    
    #show the innovation score and the class of the website
    if max_score_invest > 0.5 and max_score_doing > 0.5: 
        st.success("This company tends to be a 💰 Buyer and a 🛠️ Doer of Innovation",  icon="✅")
        st.success(f"The estimated innovation score is **{round(max(max_score_invest, max_score_doing) * 100, 2)} %**")
    elif max_score_invest > 0.5:
        st.success("This company tends to be a 💰 Buyer of Innovation",  icon="✅")
        st.success(f"The estimated innovation score is **{round(max_score_invest * 100, 2)} %**")
    elif max_score_doing > 0.5:
        st.success("This company tends to be a 🛠️ Doer of Innovation",  icon="✅")
        st.success(f"The estimated innovation score is **{round(max_score_doing * 100, 2)} %**")
    else:
        st.error(f"Not Enough hints to say that this website is innovative! The estimated innovation score is **{round(max(max_score_invest, max_score_doing) * 100, 2)} %**",  icon="❌")

    
    st.markdown("""
    <style>
    .medium-font {
        font-size:25px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display top buying sentences
    st.markdown('<p class="medium-font">Top Buying Inno Sentences:</p>', unsafe_allow_html=True)
    create_table(top_sents_invest, "invest_score")

    # Display top doing sentences
    st.markdown('<p class="medium-font">Top Doing Inno Sentences:</p>', unsafe_allow_html=True)
    create_table(top_sents_doing, "doing_score")

    # Display top negative sentences
    st.markdown('<p class="medium-font">Top Negative Sentences:</p>', unsafe_allow_html=True)
    create_table(top_sents_neg, "neg_score")
