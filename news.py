import streamlit as st
from backend import search_exact_term, find_similar_records, search_by_id
from LangchainPromptSender import LangchainPromptSender
def run():
    st.title("News")
    st.write(st.query_params["news"])
    st.write(search_by_id(st.query_params["news"]))


def display_results(results):
    for result in results:
        display_result(result)
        st.markdown("---")

def display_result(result, score_display=True):
    title = result["_source"].get("title2", "Untitled")
    text = result["_source"].get("html_text", "No text available")
    topics = result["_source"].get("topics")
    entities = result["_source"].get("entities")
    link = result["_source"].get("url", "#")
    id = result['_id']
    score = result["_score"]

    st.subheader(title)
    
    #internal_link = f'<a href="?news={id}" style="text-decoration:none;">{title}</a>'
    #st.markdown(internal_link, unsafe_allow_html=True)

    #st.write(f"{text[:200]}...")  # Cropped text to 200 chars
    st.markdown(f"{link}")

    #if isinstance(topics, list):
    #    categories = ', '.join(map(str, topics))
    #    st.write(f"**Topics/categories (auto tagging using AI):** {categories}")

    #if isinstance(entities, list):
    #    categories = ', '.join(map(str, entities))
    #    st.write(f"**Organizations mentioned (auto generation using AI):** {categories}")

    if score_display is True:
        st.write(f"**Relevance score**: {score:.2f}")
    #for record in find_similar_records(os.getenv('ELASTIC_INDEX'), id):
    #    st.write(record["_source"]['title2'])