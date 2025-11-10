import json
import os

import requests
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from unstructured.partition.html import partition_html




os.environ['BROWSERLESS_API_KEY'] = "2SJcekMEfYKmOIY90496411e7542ff717f08a0fc456b45395"

class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website: str) -> str:
    """Useful to scrape and summarize a website content"""
    url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    
    
    llm = LLM(
        #model = "openai/qwen3:4b",
        #model = "openai/qwen-mini",
        #model = "openai/deepseek-r1:7b",
        model = "openai/llama",
        #model = "openai/gemma",
        base_url="https://api.poligpt.upv.es/",
        api_key = "sk-LFXs1kjaSxtEDgOMlPUOpA",
    )

    
    summaries = []

    for chunk in chunks:
        agent = Agent(
            role='Principal Researcher',
            goal='Generate summaries from long content',
            backstory="Expert in distilling information.",
            llm=llm,
            allow_delegation=False
        )
        task = Task(
            agent=agent,
            description=f"Summarize the following content:\n\n{chunk}",
            expected_output="A clean and informative summary of the content."
        )
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        summary = crew.kickoff()
        summaries.append(str(summary))

    return "\n\n".join(summaries)
