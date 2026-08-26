from fastapi import FastAPI
from pydantic import BaseModel

from language import detect_language
from intent import detect_intent
from keywords import extract_keywords
from entities import extract_weather_entities
from datetime_extractor import extract_datetime
from location import extract_location
from domain import identify_domain_task
from parameters import extract_parameters


app = FastAPI(
    title="WeatherGPT NLP API",
    description="Multilingual Weather Query Processing",
    version="1.0"
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():

    return {
        "message": "WeatherGPT NLP API is running"
    }


@app.post("/process-query")
def process_query(request: QueryRequest):

    query = request.query

    # 1. Language
    language = detect_language(query)

    # 2. Intent
    intent = detect_intent(query)

    # 3. Keywords
    keywords = extract_keywords(query)

    # 4. Weather entities
    entities = extract_weather_entities(query)

    # 5. Date and time
    datetime_info = extract_datetime(query)

    # 6. Location
    location_name = extract_location(query)

    # 7. Domain and task
    domain_task = identify_domain_task(query)
    parameters = extract_parameters(query)

    # Final structured output
    return {

        "original_query": query,

        "language": language,

        "domain": domain_task["domain"],

        "task": domain_task["task"],

        "intent": intent,

        "keywords": keywords,

        "entities": entities,
        
        "parameters": parameters,

        "location": {
            "name": location_name
        },

        "datetime": datetime_info

    }