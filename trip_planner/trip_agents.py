from crewai import Agent, LLM
#from langchain.llms import OpenAI

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from crewai_tools import FileReadTool, FileWriterTool


import json
import os

import requests
from crewai.tools import tool



llm = LLM(
    #model = "openai/qwen3:4b",
    #model = "openai/qwen-mini",
    #model = "openai/deepseek-r1:7b",
    model = "openai/llama",
    #model = "openai/gemma",
    base_url="https://api.poligpt.upv.es/",
    api_key = "sk-LFXs1kjaSxtEDgOMlPUOpA",
)


search_internet = SearchTools.search_internet
browse = BrowserTools.scrape_and_summarize_website
calc = CalculatorTools.calculate
writeFileReceta = FileWriterTool()
readFileReceta = FileReadTool("./receta.txt")

class TripAgents():

  def escritor(self):
    return Agent(
        role='Analista profesional de Mercadona',
        goal='Resumir las quejas en datos numéricos',
        backstory=
        'Experto en ánalisis y procesamiento de datos',
        llm=llm,
        verbose=True)
  
  def agenteRecomendador(self):
    return Agent(
        role='Mercadona product expert',
        goal='Recommend Mercadona products based on client tickets and preferences',
        backstory=
        'An expert in analyzing tickets and suggesting products from Mercadona supermarket',
        tools=[ search_internet ],
        llm=llm,
        verbose=True)

  def buscador(self):
    return Agent(
        role='Recipe Searcher',
        goal='Search for recipes based on input: {input}',
        backstory="""An expert in the research capable of locating every single type of recipe""",
        tools=[
            search_internet,
            browse,
            writeFileReceta    ],
        llm=llm,
        verbose=True
        )

