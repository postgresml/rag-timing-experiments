import requests
from dotenv import load_dotenv
import time
import json
import os

# Load our environment variables
load_dotenv()
ZILLIZ_API_KEY = os.getenv("ZILLIZ_API_KEY")


# We created a simple zilliz collection called test with fields:
# primary_key - a int primary key
# vector - a vector of 384
# text a varchar


def upsert_data(documents, embeddings):
    documents = [
        {
            "vector": embedding,
            "primary_key": document["id"],
            "text": document["metadata"]["text"],
        }
        for document, embedding in zip(documents, embeddings)
    ]
    headers = {
        "Authorization": f"Bearer {ZILLIZ_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    url = (
        "https://in03-23659a0ce4651d6.api.gcp-us-west1.zillizcloud.com/v1/vector/insert"
    )
    payload = {
        "collectionName": "test",
        "data": documents,
    }
    print("\tStarting Zilliz upsert")
    tic = time.perf_counter()
    requests.post(url, data=json.dumps(payload), headers=headers)
    toc = time.perf_counter()
    time_taken_to_upsert = toc - tic
    print(f"\tDone Zilliz upsert: {time_taken_to_upsert:0.4f}")
    return time_taken_to_upsert


def do_search(vector):
    print("\tDoing cosine similarity search with Zilliz")
    url = (
        "https://in03-23659a0ce4651d6.api.gcp-us-west1.zillizcloud.com/v1/vector/search"
    )
    payload = {"collectionName": "test", "vector": vector, "outputFields": ["text"]}
    headers = {
        "Authorization": "Bearer cf555e79d3c2b3404586bc698404bb4410e3f52e5267ae2fc5cb376de2f3196b62fb88246445bb5316b6dc53d47bf6c1ee770120",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    tic = time.perf_counter()
    results = requests.post(url, data=json.dumps(payload), headers=headers).json()
    toc = time.perf_counter()
    time_done = toc - tic
    print(f"\tDone doing cosine similarity search: {time_done:0.4f}\n")
    result = results["data"][0]["text"]
    return (result, time_done)
