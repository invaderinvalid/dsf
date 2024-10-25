import requests
from django.conf import settings

def create_chat_session():
    """
    Create a new chat session with on-demand.io
    """
    url = 'https://api.on-demand.io/chat/v1/sessions'
    headers = {
        'apikey': settings.ONDEMAND_API_KEY
    }
    body = {
        "pluginIds": [],
        # "externalUserId": settings.ONDEMAND_EXTERNAL_USER_ID
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()['data']['id']
    except requests.RequestException as e:
        print(f"Error creating chat session: {e}")
        return None

def submit_query(session_id, query):
    """
    Submit a query to on-demand.io
    """
    url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    headers = {
        'apikey': settings.ONDEMAND_API_KEY
    }
    body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": query,
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error submitting query: {e}")
        return None

def get_trend_analysis(query):
    """
    Fetch trend analysis data from on-demand.io API
    """
    session_id = create_chat_session()
    if not session_id:
        return None

    response_data = submit_query(session_id, f"Analyze trends for: {query}")
    if not response_data:
        return None

    # Process the response data to extract relevant trend analysis information
    # This will depend on the structure of the response from on-demand.io
    # For now, we'll return the raw response
    return response_data

def get_trending_topics():
    """
    Fetch trending topics from on-demand.io API
    """
    session_id = create_chat_session()
    if not session_id:
        return None

    response_data = submit_query(session_id, "What are the current trending topics?")
    if not response_data:
        return None

    # Process the response data to extract trending topics
    # This will depend on the structure of the response from on-demand.io
    # For now, we'll return the raw response
    return response_data

def categorize_file(file_content, file_name):
    """
    Categorize a file using on-demand.io API
    """
    session_id = create_chat_session()
    if not session_id:
        return None

    query = f"Categorize this file: {file_name}. File content: {file_content[:1000]}..."  # Limit content to first 1000 characters
    response_data = submit_query(session_id, query)
    if not response_data:
        return None

    # Extract the category from the response
    # This might need adjustment based on the actual response structure
    category = response_data.get('data', {}).get('content', 'Uncategorized')
    return category
