import streamlit as st
from news import display_results, display_result
from backend import search_exact_term, find_similar_records
from LangchainPromptSender import LangchainPromptSender
import os

def run(company):
    if company:
        st.title(company + ' - summary')
        results = search_exact_term(os.getenv('ELASTIC_INDEX'), 'entities.keyword', company)

        prompt_template = """
            How "{company}" is related to following text? Reply shortly.
            Text:
            {text}
            """
        
        for result in results:
            variables = {
                "text": result["_source"].get("html_text", "No text available"),
                "company": company
            }
            display_result(result, False)
            with st.spinner(f'Analyzing news for {company} context'):
                prompt_sender = LangchainPromptSender("", os.getenv('OPENAI_KEY'))
                prompt_sender.send_prompt(prompt_template, variables)
                st.write(f"""**How "{company}" is related to this news? (AI generated):** {prompt_sender.get_content()}""")
            st.markdown("---")
            