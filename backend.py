from elasticsearch import Elasticsearch
import os

# Elasticsearch connection setup (replace with your credentials)
ELASTIC_HOST = os.getenv('ELASTIC_HOST')
ELASTIC_USERNAME = os.getenv('ELASTIC_USERNAME')
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
index = os.getenv('ELASTIC_INDEX')

# Initialize Elasticsearch client
es = Elasticsearch(
    [ELASTIC_HOST],
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
)

def search_by_id(id):
    response = es.get(index=index, id=id)
    return response

def search_elasticsearch(query):
    try:
        # Elasticsearch search query
        response = es.search(
            index=index,  # Replace with your index name
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["html_text"]  # Adjust based on your index schema
                    }
                },
                "size": 10
            }
        )

        # Return the hits from Elasticsearch
        return response["hits"]["hits"]
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
def get_unique_terms_and_count(index_name, field_name, min_doc_count=2):
    # Define aggregation query to count unique terms
    body = {
        "size": 0,  # We don't need to retrieve actual documents, just aggregation results
        "aggs": {
            "unique_terms": {
                "terms": {
                    "field": field_name,
                    "size": 10000,  # Adjust size based on your expected number of unique terms
                    "min_doc_count": min_doc_count,
                    "order": {
                        "_count": "asc"  # Sort by count in descending order
                    }
                }
            }
        }
    }
    
    # Run the query
    response = es.search(index=index_name, body=body)
    
    # Extract terms and their counts
    terms = response['aggregations']['unique_terms']['buckets']
    term_count = [(term['key'], term['doc_count']) for term in terms]
    print(term_count)
    return term_count

def find_similar_records(index_name, doc_id):
    """
    Find the top 3 records most similar to the given document based on 'topics.keyword' and 'html_text'.

    :param es: Elasticsearch client instance.
    :param index_name: Name of the Elasticsearch index.
    :param doc_id: ID of the current record.
    :return: List of the top 3 similar records.
    """
    # Step 1: Get the current record
    current_doc = es.get(index=index_name, id=doc_id)
    
    if not current_doc or '_source' not in current_doc:
        return f"Document with ID {doc_id} not found in index {index_name}."
    
    # Extract topics and html_text from the current document
    topics = current_doc['_source'].get('topics', [])
    html_text = current_doc['_source'].get('html_text', "")

    # Step 2: Construct the query
    query = {
        "bool": {
            "must": [
                {
                    "more_like_this": {
                        "fields": ["html_text"],
                        "like": html_text,
                        "min_term_freq": 1,
                        "max_query_terms": 12
                    }
                },
                {
                    "terms": {
                        "topics.keyword": topics
                    }
                }
            ]
        }
    }
    
    # Step 3: Perform the search for similar records
    response = es.search(
        index=index_name,
        body={
            "query": query,
            "size": 3  # Limit to the top 3 results
        }
    )
    
    # Step 4: Extract and return the top 3 similar records
    similar_records = response['hits']['hits']
    return similar_records

def search_exact_term(index, field, term, size=10):
    """
    Search for documents in Elasticsearch with an exact match for a given term in a specified field.
    
    Parameters:
    es_client (Elasticsearch): The Elasticsearch client object.
    index (str): The name of the Elasticsearch index to search in.
    field (str): The field name where the term should match.
    term (str): The exact term to match in the specified field.
    size (int): The maximum number of records to return. Default is 10.
    
    Returns:
    dict: The search results from Elasticsearch.
    """
    query = {
        "query": {
            "term": {
                field: {
                    "value": term
                }
            }
        }
    }
    
    response = es.search(index=index, body=query, size=size)
    return response['hits']['hits']