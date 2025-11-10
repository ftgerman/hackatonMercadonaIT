from crewai import Agent, LLM
#from langchain.llms import OpenAI

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools


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

class TripAgents():

  def agenteRecomendador(self):
    return Agent(
        role='Mercadona product expert',
        goal='Recommend Mercadona products based on client tickets and preferences',
        backstory=
        'An expert in analyzing tickets and suggesting products from Mercadona supermarket',
        tools=[ search_internet ],
        llm=llm,
        verbose=True)

  def cocinero(self):
    return Agent(
        role='Expert Cook',
        goal='Provide the ingredients given a certain recipe',
        backstory="""A very reknown cook""",
        tools=[
            search_internet,
            browse    ],
        llm=llm,
        verbose=True)
    
  def buscador(self):
    return Agent(
        role='Recipe Searcher',
        goal='Search for recipes based on input: {input}',
        backstory="""An expert in the research capable of locating every single type of recipe""",
        tools=[
            search_internet,
            browse    ],
        llm=llm,
        verbose=True)

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            search_internet,
            browse, calc  ],
        llm=llm,
        verbose=True)
