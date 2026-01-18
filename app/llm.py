import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def generate_summary(stats_data):
    """Generate natural language summary using OpenRouter API"""
    if not OPENROUTER_API_KEY:
        return "OpenRouter API key not configured. Please set OPENROUTER_API_KEY in .env file."
    
    prompt = f"""
    Analyze this dataset and provide a concise summary in plain English:
    
    Dataset Info:
    - Shape: {stats_data.get('shape', 'Unknown')}
    - Columns: {', '.join(stats_data.get('columns', []))}
    - Missing values: {stats_data.get('missing_values', {})}
    
    Provide insights about the data quality, key patterns, and recommendations in 2-3 sentences.
    """
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Error generating summary: {response.status_code}"
    
    except Exception as e:
        return f"Error connecting to OpenRouter: {str(e)}"