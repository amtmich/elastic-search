import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from backend import search_elasticsearch, get_unique_terms_and_count, find_similar_records
from news import display_results

def load_news():
    import news
    news.run()

def load_company(company_name):
    import company
    company.run(company_name)

def load_topic(topic_name):
    import topic
    topic.run(topic_name)

def create_selectbox(key, label, placeholder, data_fetch_function, *args):
    options = [placeholder] + [item[0] for item in data_fetch_function(*args)]
    select = st.selectbox(label, options)
    return select

# Streamlit frontend
def main():
    st.sidebar.image(os.getenv('LOGO'), use_column_width=True)
    st.sidebar.title("Choose action:")
    semantic = st.sidebar.button("Semantic search")
    organizations = st.sidebar.button("Organizations summary")
    topics = st.sidebar.button("Topic summary")

    # Variable to track which button is active
    if semantic:
        st.session_state['active'] = 1
    elif organizations:
        st.session_state['active'] = 2
    elif topics:
        st.session_state['active'] = 3

    if 'active' in st.session_state:
        if st.session_state['active'] == 1:
            query = st.text_input("Enter your search query for semantic search and press button below:")
            search = st.button("Search")
            if search:
                if query:
                    # Display search results
                    with st.spinner("Searching..."):
                        results = search_elasticsearch(query)
                        if results:
                            display_results(results)
                        else:
                            st.warning("No results found!")
                else:
                    st.warning("Please enter a search query.")
        elif st.session_state['active'] == 2:
            company = create_selectbox(
                "company",
                'Choose an organization - so that you will get news that are related to that organization as well as some explanation:',
                '',
                get_unique_terms_and_count,
                os.getenv('ELASTIC_INDEX'),
                'entities.keyword'
                )
            load_company(company)
        elif st.session_state['active'] == 3:
            topic = create_selectbox("topic", 'Choose a topic - so that you will get news that are related to that topic as well as some explanation:', '', get_unique_terms_and_count, os.getenv('ELASTIC_INDEX'), 'topics.keyword')
            load_topic(topic)
    else:
        st.header("Choose action from left menu.")


#    if "topic" not in st.query_params and "company" not in st.query_params and "news" not in st.query_params:
#        if st.sidebar.button(':leftwards_arrow_with_hook:',key="1"):
#            query_params = {}
#            st.experimental_set_query_params(**query_params)

if __name__ == "__main__":
    main()
