import os
import json
from pathlib import Path
from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods
import re
# Library for watsonx.data we will call out to Watsonx.data to grab Milvus vectorized information

load_dotenv()

# tried "ibm/granite-13b-instruct-v2" as first option
def send_to_watsonx(text_path: Path, prompt: str, model_id: str = "mistralai/mixtral-8x7b-instruct-v01"):
    """
    Sends extracted document text and a prompt to Watsonx.ai using the IBM SDK.

    Args:
        text_path (Path): Path to the extracted text file.
        prompt (str): The prompt to send to the AI model.
        model_id (str): WatsonX model ID to use (default: 'ibm/ibm/llama-2-70b-chat')
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    
    if not api_key:
        raise ValueError("Please set the WATSONX_API_KEY environment variable.")

    # Load extracted text content
    with open(text_path, 'r', encoding='utf-8') as f:
        text_content = f.read().strip()
    
    print("\n===== WatsonX Request Debugging =====")
    print(f"Model: {model_id}")
    print(f"Extracted Text Sent:\n{'='*40}\n{text_content[:500]}...\n{'='*40}")
    print(f"Prompt Sent:\n{'='*40}\n{prompt}\n{'='*40}")
    print(f"Text Length: {len(text_content)} characters")
    print("=====================================")

    prompt_input = f"""Context: The following is extracted text from a document, including tables and lists:\n\n{text_content}\n\nPrompt: {prompt}"""

    print("\n===== Final Input to WatsonX =====")
    print(prompt_input[:1100])  # Print only first 1000 characters for readability
    print("=================================")

    params = {
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.MAX_NEW_TOKENS: 1000,
        GenParams.MIN_NEW_TOKENS: 50,
        GenParams.TEMPERATURE: 0.1,
        GenParams.REPETITION_PENALTY: 1.1
    }

    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": api_key
    }

    model = Model(
        model_id=model_id,
        params=params,
        credentials=credentials,
        project_id=project_id
    )

    try:
        response = model.generate(prompt=prompt_input)

        
        
        
        
        print("\n===== AI Response =====")
        # print(response)
        # Extract generated text
        generated_text = response["results"][0]["generated_text"]

        # Extract JSON part
        start = generated_text.find("[")
        end = generated_text.rfind("]") + 1
        # if start != -1 and end != -1:
        extracted_json = generated_text[start:end]
        print('Output of the extracted info: ', extracted_json)
        print("-------------------------------------------------------------------------")
        # Save AI response to a file
        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        response_file = output_dir / "watsonx_response.json"
        # extracted_data = json.loads(extracted_json)
        with open(response_file, "w", encoding="utf-8") as f:
            json.dump(extracted_json, f, indent=2)
        print(f"AI response saved to {response_file}")
        # else:
        #     print("No JSON output found.")
        print("=======================")

        # # Save AI response to a file
        # output_dir = Path("output")
        # output_dir.mkdir(parents=True, exist_ok=True)
        # response_file = output_dir / "watsonx_response.json"
        # # extracted_data = json.loads(extracted_json)
        # with open(response_file, "w", encoding="utf-8") as f:
        #     json.dump(extracted_json, f, indent=2)
        # print(f"AI response saved to {response_file}")

        # Extract generated text and clean up JSON
        generated_text = response.get("results", [{}])[0].get("generated_text", "")
        cleaned_text = re.sub(r"^Output:\s*", "", generated_text).strip()
        cleaned_text = cleaned_text.replace("\n", "")  # Remove all newline escape characters
        
        # Save cleaned text for debugging
        debug_text_file = output_dir / "watsonx_cleaned_text.json"
        with open(debug_text_file, "w", encoding="utf-8") as f:
            f.write(extracted_json)
        print(f"Cleaned WatsonX text saved to {debug_text_file}")
        
        # # Fix duplicate keys by converting JSON string to a dictionary list
        # try:
        #     json_data = json.loads(cleaned_text)  # Convert text to JSON
        #     structured_json = []
        #     for entry in json_data:
        #         structured_entry = {key: value for key, value in entry.items() if key != "PREMIUM"}
        #         structured_entry["PREMIUM"] = entry.get("PREMIUM", "")  # Keep only the last premium value
        #         structured_json.append(structured_entry)
            
        #     structured_file = output_dir / "watsonx_structured.json"
        #     with open(structured_file, "w", encoding="utf-8") as f:
        #         json.dump(structured_json, f, indent=2)
        #     print(f"Structured JSON saved to {structured_file}")
        # except json.JSONDecodeError as e:
        #     print(f"Failed to parse generated text into JSON: {e}")

        return response
    
    except Exception as e:
        print(f"Request failed: {e}")
        raise
