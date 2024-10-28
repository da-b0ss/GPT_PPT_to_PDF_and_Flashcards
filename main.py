import comtypes.client
import os
import sys
import subprocess
import re
from pathlib import Path
from voice import convert_text_to_mp3_pyttsx3

# [Previous functions remain the same: ppt_to_pdf_default, ppt_to_pdf_custom, process_folder, run_ai_script]

def extract_page_content(content):
    """
    Extract page content from the transcript format with PAGE markers.
    Returns a list of tuples (page_number, content).
    """
    # Match content between PAGE markers
    pattern = r'PAGE (\d+):\n-{20}\n(.*?)\n-{20}'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    pages = []
    for match in matches:
        page_num = match.group(1)
        page_content = match.group(2).strip()
        if page_content:  # Only include non-empty pages
            pages.append((page_num, page_content))
    
    return pages

def create_audio_from_transcript(transcript_path):
    """
    Create MP3 files for each page in a transcript file.
    """
    print(f"\nProcessing transcript: {transcript_path}")
    
    # Read the transcript content
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(transcript_path, 'r', encoding='latin-1') as f:
            content = f.read()

    # Create audio directory structure
    pdf_name = Path(transcript_path).stem
    base_audio_dir = "audio"
    pdf_audio_dir = os.path.join(base_audio_dir, pdf_name)
    
    # Create directories if they don't exist
    os.makedirs(pdf_audio_dir, exist_ok=True)

    # Extract pages and their content
    pages = extract_page_content(content)
    
    if not pages:
        print(f"No valid page content found in {transcript_path}")
        return

    # Process each page
    for page_num, page_content in pages:
        if page_content.strip():
            # Create temporary text file for the page content
            temp_txt_path = os.path.join(pdf_audio_dir, f"temp_page_{page_num}.txt")
            with open(temp_txt_path, 'w', encoding='utf-8') as f:
                f.write(page_content)

            # Convert to MP3
            output_mp3 = os.path.join(pdf_audio_dir, f"{pdf_name}_page{page_num}.mp3")
            try:
                convert_text_to_mp3_pyttsx3(temp_txt_path, output_mp3)
                print(f"Created audio for page {page_num}: {output_mp3}")
            except Exception as e:
                print(f"Error creating audio for page {page_num}: {str(e)}")
            finally:
                # Clean up temporary text file
                if os.path.exists(temp_txt_path):
                    os.remove(temp_txt_path)

def process_all_transcripts():
    """
    Process all transcript files in the Transcripts directory
    """
    transcripts_dir = "Transcripts"
    if not os.path.exists(transcripts_dir):
        print("No transcripts directory found.")
        return

    print("\nProcessing transcripts to create audio files...")
    
    transcript_files = [f for f in os.listdir(transcripts_dir) if f.endswith('.txt')]
    if not transcript_files:
        print("No transcript files found in the Transcripts directory.")
        return

    for transcript_file in transcript_files:
        transcript_path = os.path.join(transcripts_dir, transcript_file)
        create_audio_from_transcript(transcript_path)

def create_brainrot_lectures():
    try:
        import ai
        pdf_folder = "PDF"
        if not os.path.exists(pdf_folder):
            print(f"Error: PDF folder '{pdf_folder}' does not exist.")
            return
            
        print("Creating Brainrot Lectures...")
        ai.process_all_pdfs_brainrot(pdf_folder)
        print("Brainrot Lectures have been created in the 'Transcripts' folder")
        
        # After creating transcripts, process them into audio files
        process_all_transcripts()
        print("\nAudio files have been created in the 'audio' directory")
        
    except Exception as e:
        print(f"Error creating Brainrot Lectures: {e}")

def get_user_choice(prompt, valid_options):
    while True:
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(valid_options)}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, 'PPTX')
    output_folder = os.path.join(script_dir, 'PDF')

    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)

    while True:
        print("\nPowerPoint to PDF Converter with AI Analysis")
        print("=" * 40)
        print("1. Generate default PDFs")
        print("2. Generate custom PDFs")
        print("3. Run AI Analysis")
        print("4. Make Brainrot Lectures")
        print("5. Create Audio (from existing transcripts)")  # Added new option
        print("Type 'EXIT!' to quit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice.upper() == 'EXIT!':
            print("Exiting program...")
            break
            
        if choice == '1':
            process_folder(input_folder, output_folder, use_custom=False)
        elif choice == '2':
            process_folder(input_folder, output_folder, use_custom=True)
        elif choice == '3':
            run_ai_script()
        elif choice == '4':
            create_brainrot_lectures()
        elif choice == '5':
            process_all_transcripts()  # Added new option to process existing transcripts
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()