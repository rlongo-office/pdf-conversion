from pathlib import Path
import json
from pprint import pprint

def find_table_elements(document_content):
    """Find all elements that might be part of our target table."""
    
    table_elements = []
    
    def process_node(node):
        if isinstance(node, dict):
            # Look for text nodes
            if "text" in node:
                text = node["text"]
                # Store nodes with business-related text or X marks
                if (text.isupper() and len(text) > 3) or text == "X" or text == "x":
                    if "prov" in node and node["prov"]:
                        bbox = node["prov"][0].get("bbox")
                        table_elements.append({
                            "text": text,
                            "bbox": bbox,
                            "y": bbox["t"] if bbox else 0
                        })
            
            # Recurse through children
            if "children" in node:
                for child in node["children"]:
                    process_node(child)
        elif isinstance(node, list):
            for item in node:
                process_node(item)
    
    process_node(document_content)
    
    # Sort elements by vertical position
    table_elements.sort(key=lambda x: -x["y"])
    return table_elements

def main():
    # Load the JSON file
    json_path = Path("output") / "sample.json"
    with open(json_path, 'r') as f:
        document_content = json.load(f)
    
    # Find potential table elements
    elements = find_table_elements(document_content)
    
    print("\nPotential table elements found:")
    print("===============================")
    for elem in elements:
        print(f"Text: {elem['text']:<20} Y-pos: {elem['y']:<10} X-pos: {elem['bbox']['l']}")

if __name__ == "__main__":
    main() 