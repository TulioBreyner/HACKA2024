from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import redis

HOST = 'localhost'
PORT = 6379

embedder = SentenceTransformer("msmarco-distilbert-base-v4")
client = redis.Redis(HOST, PORT, decode_responses=True)

# if client.ping() != "PONG":
#     print("Ping... NOT PONG")
#     exit(1)

QUERY = (
    Query('(*)=>[KNN 3 @vector $query_vector AS vector_score]')
     .sort_by('vector_score')
     .return_fields('vector_score', 'id', 'authors', 'title', 'year', 'link')
     .dialect(2)
)

def search(query):
    encoded_query = embedder.encode(query)
    response = client.ft('idx:articles_vss').search(
        QUERY,
        {
        'query_vector': np.array(encoded_query, dtype=np.float32).tobytes()
        }
    ).docs

    results = []

    for doc in response:
        vector_score = round(1 - float(doc.vector_score), 2)
        results.append({
            "query": query,
            "score": vector_score,
            "id": doc.id,
            "title": doc.title,
            "authors": doc.authors,
            "year": doc.year,
            "link": doc.link,
        })
    
    return results
