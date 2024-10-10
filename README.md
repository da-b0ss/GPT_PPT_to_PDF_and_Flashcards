# PowerPoint to PDF Converter with AI Analysis

This project converts PowerPoint presentations to PDF and optionally performs AI analysis on the generated PDFs.

## Dependencies

Install the required packages:

## Setup

1. Clone the repository
2. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

1. Place your PowerPoint files (.pptx) in the `PPTX` folder
2. Run `python main.py`
3. Choose conversion options:
   - Default PDF (1 slide per page)
   - Custom PDF (includes notes, hidden slides, etc.)
4. Optionally run AI analysis on the generated PDFs

## Documentation

For details on the custom PDF export options, see [Microsoft's PowerPoint VBA documentation](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.presentation.exportasfixedformat).
