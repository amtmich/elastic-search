import os
from dotenv import load_dotenv, dotenv_values 
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import time

load_dotenv() 

class LangchainPromptSender:
    def __init__(self, llm = "", api_key = ""):
        if llm == "":
            self.llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)
        else:
            self.llm = llm

    def send_prompt(self, prompt_template, variables = {}):
        prompt = PromptTemplate(template=prompt_template, input_variables=list(variables.keys()))
        formatted_prompt = prompt.format(**variables)
        response = self.llm.invoke(formatted_prompt)
        self.response = response
        return self.response
    
    def get_content(self):
        return self.response.content