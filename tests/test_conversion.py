import pytest
from pathlib import Path
from src.convert import extract_content
from src.watsonx_integration import send_to_watsonx
import json
import requests

@pytest.fixture
def test_pdf():
    # Using a sample PDF in tests/data directory
    return Path(__file__).parent / "data" / "sample.pdf"

@pytest.fixture
def output_dir():
    path = Path(__file__).parent / "output"
    path.mkdir(parents=True, exist_ok=True)
    return path

def test_pdf_conversion(test_pdf, output_dir):
    """Test the PDF conversion process"""
    # Skip if test PDF doesn't exist
    if not test_pdf.exists():
        pytest.skip("Test PDF file not found")
    
    # Test content extraction
    json_file = extract_content(test_pdf, output_dir)
    
    # Verify JSON file was created
    assert json_file.exists()
    
    # Basic validation of JSON content
    with open(json_file, 'r') as f:
        content = json.load(f)
        assert isinstance(content, dict)
        assert len(content) > 0

def test_watsonx_integration(test_pdf, output_dir, monkeypatch):
    """Test the Watsonx integration with mocked credentials"""
    # Mock environment variables
    monkeypatch.setenv("WATSONX_API_KEY", "fake_key")
    monkeypatch.setenv("WATSONX_ENDPOINT", "https://fake-endpoint.com")
    
    # Extract content first
    json_file = extract_content(test_pdf, output_dir)
    
    # Test sending to Watsonx (this will fail without real credentials)
    with pytest.raises(requests.exceptions.RequestException):
        send_to_watsonx(json_file, "Test prompt") 