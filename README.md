# SmartStudy - A PowerPoint to PDF Converter with AI Analysis and Video Generation

This project converts PowerPoint presentations to PDF, performs AI analysis to create simplified explanations, and generates educational videos with voiceovers.

## Features
- Convert PowerPoint presentations to PDF
- AI-powered content analysis and simplification
- Text-to-speech audio generation
- Automatic video creation from slides and audio
- Generate study materials with term-definition pairs

## Dependencies
Install all required packages using the command:

```bash
pip install comtypes PyPDF2 python-dotenv requests cryptography gtts playsound pydub moviepy PyMuPDF pyttsx3 pathlib
```

## Setup
1. Clone the repository
2. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`
3. Create the following directory structure:
   ```
   project_root/
   ├── PPTX/           # Input PowerPoint files
   ├── PDF/            # Generated PDFs
   ├── Transcripts/    # AI-generated explanations
   ├── audio/          # Generated audio files
   └── Short-Form-Videos/  # Final video outputs
   ```

## Usage
Run `python main.py` and choose from the following options:

1. **Generate default PDFs**
   - Converts PowerPoint files to basic PDFs (1 slide per page)

2. **Generate custom PDFs**
   - Enhanced PDF conversion with notes, hidden slides, and additional features

3. **Run AI Analysis**
   - Analyzes PDFs and generates term-definition pairs
   - Creates a `pairs.txt` file with study materials

4. **Make Short-Form Content Lectures**
   - Creates simplified explanations of each slide
   - Generates memorization techniques and examples
   - Saves explanations in the Transcripts folder

5. **Create Audio and Videos**
   - Converts text explanations to speech
   - Combines slide images with audio
   - Creates educational videos for each slide

## File Structure
- `main.py`: Main program with user interface and PowerPoint conversion
- `ai.py`: Handles AI analysis and content generation
- `voice.py`: Text-to-speech conversion utilities

## Voice Configuration
The project supports two text-to-speech engines:
- Google Text-to-Speech (gTTS): Better quality, internet required
- pyttsx3: Offline capability, adjustable speech rate

To list available voices:
```bash
python voice.py --list-voices
```

## Custom PDF Export Options
The custom PDF generation includes:
- Notes pages
- Hidden slides
- Document properties
- Document structure tags
- High-quality bitmap fonts

For detailed export options, see [Microsoft's PowerPoint VBA documentation](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.presentation.exportasfixedformat).

## Output Files
- `PDF/`: Contains converted PDF files
- `Transcripts/`: Contains AI-generated explanations
- `audio/`: Contains generated MP3 files for each slide
- `Short-Form-Videos/`: Contains final videos with slides and voiceover
- `pairs.txt`: Term-definition pairs for study materials

## Requirements
- Windows OS (for PowerPoint automation)
- Python 3.6 or higher
- Microsoft PowerPoint installed
- Internet connection (for OpenAI API and gTTS)

## Troubleshooting
1. **PowerPoint Automation**
   - Ensure Microsoft PowerPoint is installed
   - Run the script with appropriate permissions

2. **Audio Generation**
   - Check audio device settings
   - Try alternative voice engine if one fails

3. **Video Creation**
   - Ensure sufficient disk space
   - Check write permissions in output directories

4. **API Issues**
   - Verify OpenAI API key in `.env`
   - Check internet connection
   - Monitor API usage limits
