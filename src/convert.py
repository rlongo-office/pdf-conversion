from pathlib import Path
import json
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.document_converter import PdfFormatOption

def extract_content(pdf_path: Path, output_dir: Path) -> Path:
    """
    Converts a PDF document to JSON with enhanced table extraction settings.

    Args:
        pdf_path (Path): Path to the PDF document.
        output_dir (Path): Directory to save the output files.

    Returns:
        Path: Path to the exported JSON file.
    """
    # Configure advanced table extraction
    pipeline_options = PdfPipelineOptions(do_table_structure=True)
    pipeline_options.table_structure_options.do_cell_matching = False  # Use detected text cells
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE  # More accurate table extraction

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = converter.convert(pdf_path)

    # Export to JSON
    json_output = output_dir / f"{pdf_path.stem}.json"
    content = result.document.export_to_dict()

    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2)
        print(f"Exported JSON to {json_output}")

    return json_output
