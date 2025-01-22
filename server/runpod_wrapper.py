import runpod
from typing import Any, TypedDict
import requests
import sys


class HandlerInput(TypedDict):
    """The data for calling the Ollama service."""

    method_name: str
    """The url endpoint of the Ollama service to make a post request to."""

    input: Any
    """The body of the post request to the Ollama service."""


class HandlerJob(TypedDict):
    input: HandlerInput


def handler(job: HandlerJob):
    base_url = "http://0.0.0.0:11434"
    input_data = job["input"]
    
    try:
        # Ensure input is properly formatted
        if "stream" in input_data["input"]:
            input_data["input"]["stream"] = False
            
        # Get model from command line or default
        model = sys.argv[1] if len(sys.argv) > 1 else "mistral"
        input_data["input"]["model"] = model
        
        # Make request to Ollama
        response = requests.post(
            url=f"{base_url}/{input_data['method_name']}",
            headers={"Content-Type": "application/json"},
            json=input_data["input"],
        )
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"response": response.text}
            
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
