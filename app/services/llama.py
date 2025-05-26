import requests

async def generate_summary(content: str) -> str:
    url = "http://host.docker.internal:11434/api/generate"
    payload = {
        "model": "llama3.1:8b",
        "prompt": f"Summarize the following content: {content}",
        "stream": False

    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]