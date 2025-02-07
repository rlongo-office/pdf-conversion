from pathlib import Path
import json
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.document_converter import PdfFormatOption

# Add API call to watsonx.data and have it store the JSON in the Milvus

def extract_content(pdf_path: Path, output_dir: Path) -> dict:
    """
    Converts a PDF document to JSON and extracts rich text format.

    Args:
        pdf_path (Path): Path to the PDF document.
        output_dir (Path): Directory to save the output files.

    Returns:
        dict: Paths to the exported JSON and text file.
    """
    # Configure pipeline options with advanced table structure detection
    pipeline_options = PdfPipelineOptions(do_table_structure=True)
    pipeline_options.table_structure_options.do_cell_matching = False
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = converter.convert(pdf_path)

    # Export JSON
    json_output = output_dir / f"{pdf_path.stem}.json"
    content = result.document.export_to_dict()
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2)
    print(f"Exported JSON to {json_output}")

    # Clean and Export rich text representation
    raw_text = result.document.export_to_text()
    
    # Clean text: Remove leading/trailing whitespaces from each line and remove blank lines
    cleaned_text = "\n".join(
        line.strip() for line in raw_text.splitlines() if line.strip()
    )

    text_output = output_dir / f"{pdf_path.stem}_rich_text.txt"
    with open(text_output, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"Exported Cleaned Rich Text to {text_output}")

    return {"json_path": json_output, "text_path": text_output}  # Return both paths as a dictionary
