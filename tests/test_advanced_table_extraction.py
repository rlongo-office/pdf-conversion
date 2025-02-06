
from pathlib import Path
import sys

# Add src/ to sys.path dynamically
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
import json
from src.convert import extract_content


def test_table_extraction():
    """
    Run a PDF through Docling's advanced table extraction and inspect the output.
    """
    pdf_path = Path("tests/data/first_page.pdf")  # Replace with your test PDF file
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_output = extract_content(pdf_path, output_dir)

    # Load extracted JSON
    with open(json_output, "r", encoding="utf-8") as f:
        extracted_data = json.load(f)

    # Check if tables are detected in the document
    if "tables" in extracted_data:
        print("\nExtracted Tables:")
        for i, table in enumerate(extracted_data["tables"]):
            print(f"\nTable {i+1}:")
            for row in table.get("rows", []):
                print(" | ".join(cell.get("text", "") for cell in row))
    else:
        print("\nNo tables detected!")

if __name__ == "__main__":
    test_table_extraction()
