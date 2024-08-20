import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()


def format_list_as_json(list):

    #format list as json
    json_list = []
    for item in list:
        json_list.append(json.dumps(item))

    return json_list



def get_embeddings(input_list):

    json_input = format_list_as_json(input_list)

    url = 'https://api.jina.ai/v1/embeddings'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ os.getenv('JINA_TOKEN')
    }

    data = {
        "model": "jina-clip-v1",
        "normalized": True,
        "embedding_type": "float",
        "input": [
            json_input
            #expected format: {"text": "A blue cat"}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    print(response)

    return response