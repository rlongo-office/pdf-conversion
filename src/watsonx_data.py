import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def __init__(self):
        """
        Initializes the Watsonx.data API connection using environment variables.
        """
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.base_url = os.getenv("WATSONX_DATA_API_URL")  # Example: https://api.us-south.watsonxdata.cloud.ibm.com
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }