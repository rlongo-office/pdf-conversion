# Document Conversion and AI Integration Project

This project uses **Docling** to convert documents into structured data and integrates with **IBM watsonx.ai** models for advanced processing.

## Features

- Convert PDFs and other document formats to JSON and Markdown.
- Integrate with IBM watsonx.ai models like Granite and Llama.
- Batch processing of documents.
- Export structured data for LLMs and databases.

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Set Up the Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file and add your Watsonx.ai API credentials.

   ```env
   WATSONX_API_KEY=your_watsonx_api_key
   WATSONX_ENDPOINT=https://api.watsonx.ai/v1
   ```

5. **Run the Project**

   ```bash
   python src/main.py
   ```

## Usage

Describe how to use your scripts, provide examples, etc.

## Contributing

Guidelines for contributing to the project.

## License

Specify the license.
