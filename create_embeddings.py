import requests
import os
import json
from dotenv import load_dotenv

load_dotenv("config.env")


def get_embeddings(input_list):

    formatted_data = [{"text": item} for item in input_list]

    # Convert to JSON string
    json_string = json.dumps(formatted_data)
    print(json_string)

    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + str(os.getenv("JINA_TOKEN")),
    }

    data = {
        "model": "jina-clip-v1",
        "normalized": True,
        "embedding_type": "float",
        "input": json_string,
        # expected format: {"text": "A blue cat"}
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

    return response.text


print(get_embeddings(["A blue cat", "A red cat"]))
