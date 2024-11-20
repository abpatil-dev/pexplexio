import os
import re
import subprocess
import json
import pytz
from datetime import datetime
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from prompt_templates import *
load_dotenv()

COUNTRY_TIMEZONES = {
    "United States": "America/New_York",
    "India": "Asia/Kolkata",
    "United Kingdom": "Europe/London",
    "Australia": "Australia/Sydney",
    "Canada": "America/Toronto",
    "Germany": "Europe/Berlin",
    "China": "Asia/Shanghai",
    "Brazil": "America/Sao_Paulo",
    "South Africa": "Africa/Johannesburg"
}

def get_local_time(country):
    timezone_name = COUNTRY_TIMEZONES.get(country)
    if not timezone_name:
        return f"Time zone for {country} is not defined."
    timezone = pytz.timezone(timezone_name)
    local_time = datetime.now(timezone)
    formatted_local_time = local_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    return formatted_local_time

def get_answer_status(llm, user_query, history,dt_time):
    parser = JsonOutputParser(pydantic_object=llm_status)

    prompt = PromptTemplate(
        template = STATUS_TEMPLATE,
        input_variables = ["query","history","yes","no","dt_time"],
        partial_variables = {"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm
    unparsed_output = chain.invoke({
        "query": user_query, "history": history,
        'yes': '{"status" : "YES", answer : "Whatever the actual answer is.... "}',
        'no': '{"status" : "NO", answer : "Whatever the new fomatted question is.... "}',
        'dt_time': dt_time
        })
    
    unparsed_output = unparsed_output.content
    json_pattern = r'\{(?:[^{}]*\{[^{}]*\}[^{}]*|[^{}]*)*\}'
    unparsed_output = re.findall(json_pattern, unparsed_output)[0]
    final_status_dict = parser.parse(unparsed_output)

    return final_status_dict


def search_api(query, max_results=5):
    api_key = os.getenv("TAVILY_API_KEY")
    url = "https://api.tavily.com/search"

    payload = { 
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "topic": "general",
        "include_answer": True,
        "include_images": False,
        "include_raw_content": True,
        "max_results": max_results,
        "include_domains": [],
        "exclude_domains": []
    }
    data = json.dumps(payload)

    result = subprocess.run(
        [
            "curl", "-X", "POST", url,
            "-H", "Content-Type: application/json",
            "-d", data
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )
    return result.stdout


def get_chat_response(llm, status_dict, user_input, history, dt_time):
    if status_dict['status'] == 'YES':
        return status_dict['answer'], []
    else:
        prompt_template = (RESPONSE_TEMPLATE)

        output = search_api(query = status_dict['answer'], max_results=4)
        json_data = json.loads(output)

        if isinstance(json_data, dict) and isinstance(json_data.get('results'), list):
            reference_urls = [
                str(result.get('url', 'N/A'))  
                for result in json_data['results'] 
                if result.get('score', 0) > 0.5  
            ]
            raw_contents = [
                "Title : " + str(result.get('title', 'N/A')) + "\n" + 
                "Content : \n" + str(result.get('raw_content', 'N/A'))
                for result in json_data['results'] 
                if result.get('score', 0) > 0.5
            ]
        else:
            reference_urls = []
            raw_contents = []

        possible_answer = json_data['answer']
        reference_text = "\n\n".join(raw_contents)
        reference_text = possible_answer + '\n\n' + reference_text

        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain =  (prompt | llm | StrOutputParser())
        chat_response = chain.invoke({'query': user_input, 'reference_text': reference_text, 'history': history, 'dt_time': dt_time})
        
        return chat_response, reference_urls