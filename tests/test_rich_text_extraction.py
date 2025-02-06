import sys
from pathlib import Path
# Add src/ to sys.path dynamically
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
import json
from src.convert_text import extract_content

def test_rich_text_extraction():
    """
    Runs a PDF through Docling and extracts rich text format.
    """
    pdf_path = Path("tests/data/first_page.pdf")  # Replace with actual test PDF
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    extracted_files = extract_content(pdf_path, output_dir)  # Returns a dict

    # Read extracted rich text file
    text_path = extracted_files["text_path"]  # Now correctly accesses the dictionary
    with open(text_path, "r", encoding="utf-8") as f:
        rich_text_content = f.read()

    print("\nExtracted Rich Text Representation:")
    print("===================================")
    print(rich_text_content[:1000])  # Show only first 1000 chars for preview

if __name__ == "__main__":
    test_rich_text_extraction()

