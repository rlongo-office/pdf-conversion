import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from convert_text import extract_content
from watsonx_integration import send_to_watsonx
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context


def read_prompt_file(prompt_path: Path) -> str:
    """Read prompt from a text file."""
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text().strip()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process PDF and send to Watsonx.ai')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory')
    parser.add_argument('--prompt-file', type=str, required=True, help='Path to file containing the prompt')
    parser.add_argument('--model', type=str, default='ibm/granite-13b-instruct-v2', help='WatsonX model ID to use')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Convert string paths to Path objects
    pdf_path = Path(args.pdf_path)
    output_dir = Path(args.output_dir)
    prompt_path = Path(args.prompt_file)

    # Validate input files
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    # Read prompt from file
    prompt = read_prompt_file(prompt_path)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Extract content
        extracted_files = extract_content(pdf_path, output_dir)
        text_path = extracted_files["text_path"]  # Use text output

        print("text_path: ", text_path)
        
        # Step 2: Send to Watsonx.ai
        response = send_to_watsonx(text_path, prompt, args.model)
        print("The Final response", response)
    except Exception as e:
        print(f"Error processing document: {e}")
        raise

if __name__ == "__main__":
    main()
