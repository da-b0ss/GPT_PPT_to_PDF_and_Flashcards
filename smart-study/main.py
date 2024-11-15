import comtypes.client
import os
import sys
import subprocess
import re
from pathlib import Path
from voice import convert_text_to_mp3_pyttsx3
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
import fitz  # PyMuPDF for PDF handling


'''

pip install cryptography
pip install gtts playsound
pip install gtts pydub
pip install moviepy
pip install PyMuPDF


pip install gtts pyttsx3
'''

def ppt_to_pdf_default(input_file_name, output_file_name):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    try:
        deck = powerpoint.Presentations.Open(input_file_name)
        deck.SaveAs(output_file_name, 32)  # 32 is the format type for PDF
        print(f"Successfully converted {input_file_name} to {output_file_name}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        try:
            deck.Close()
        except:
            pass
        powerpoint.Quit()

def ppt_to_pdf_custom(input_file_name, output_file_name):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    try:
        deck = powerpoint.Presentations.Open(input_file_name)
        
        export_options = {
            "Path": output_file_name,
            "FixedFormatType": 2,  # ppFixedFormatTypePDF
            "Intent": 1,  # ppFixedFormatIntentScreen
            "OutputType": 5,  # ppPrintOutputNotesPages
            "PrintHiddenSlides": True,
            "IncludeDocProperties": True,
            "DocStructureTags": True,
            "BitmapMissingFonts": True,
        }

        deck.ExportAsFixedFormat(**export_options)
        print(f"Successfully converted {input_file_name} to {output_file_name} with custom settings")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        try:
            deck.Close()
        except:
            pass
        powerpoint.Quit()

def process_folder(input_folder, output_folder, use_custom=False):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pptx'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
            
            if use_custom:
                ppt_to_pdf_custom(input_path, output_path)
            else:
                ppt_to_pdf_default(input_path, output_path)

def run_ai_script():
    try:
        subprocess.run([sys.executable, "ai.py"], check=True)
        print("AI script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running AI script: {e}")

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

def extract_page_from_pdf(pdf_path, page_number, output_path):
    """
    Extract a single page from a PDF and save it as an image
    """
    try:
        doc = fitz.open(pdf_path)
        page = doc[page_number]
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
        pix.save(output_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Error extracting PDF page: {str(e)}")
        return False

def create_video_from_image_and_audio(image_path, audio_path, output_path):
    """
    Create a video from a still image and an audio file
    """
    try:
        # Load the audio to get its duration
        audio = AudioFileClip(audio_path)
        
        # Create video from the image with the same duration as the audio
        video = ImageClip(image_path).set_duration(audio.duration)
        
        # Combine video and audio
        final_video = video.set_audio(audio)
        
        # Write the video file
        final_video.write_videofile(output_path, 
                                  fps=1,  # 1 fps is enough for still image
                                  codec='libx264',
                                  audio_codec='aac')
        
        # Close the clips
        audio.close()
        video.close()
        final_video.close()
        
        return True
    except Exception as e:
        print(f"Error creating video: {str(e)}")
        return False

def process_pdf_to_videos(pdf_path, audio_dir, video_dir):
    """
    Create videos for each page of a PDF with corresponding audio
    """
    pdf_name = Path(pdf_path).stem
    pdf_video_dir = os.path.join(video_dir, pdf_name)
    os.makedirs(pdf_video_dir, exist_ok=True)
    
    # Temporary directory for page images
    temp_img_dir = os.path.join(pdf_video_dir, "temp_images")
    os.makedirs(temp_img_dir, exist_ok=True)
    
    try:
        # Get list of audio files and extract their actual page numbers
        audio_files = []
        for f in os.listdir(os.path.join(audio_dir, pdf_name)):
            if f.endswith('.mp3'):
                # Extract the page number from the filename
                match = re.search(r'page(\d+)', f)
                if match:
                    audio_files.append((f, int(match.group(1))))
        
        # Sort by page number
        audio_files.sort(key=lambda x: x[1])
        
        for audio_file, actual_page_num in audio_files:
            # Paths setup
            audio_path = os.path.join(audio_dir, pdf_name, audio_file)
            img_path = os.path.join(temp_img_dir, f"page_{actual_page_num}.png")
            video_path = os.path.join(pdf_video_dir, f"{pdf_name}_page{actual_page_num}.mp4")
            
            print(f"\nProcessing page {actual_page_num} of {pdf_name}")
            
            # Extract PDF page as image (subtract 1 from page_num for 0-based index)
            if extract_page_from_pdf(pdf_path, actual_page_num - 1, img_path):
                # Create video
                if create_video_from_image_and_audio(img_path, audio_path, video_path):
                    print(f"Created video: {video_path}")
                else:
                    print(f"Failed to create video for page {actual_page_num}")
            else:
                print(f"Failed to extract page {actual_page_num} from PDF")
                
            # Clean up temporary image
            if os.path.exists(img_path):
                os.remove(img_path)
                
        # Clean up temporary image directory
        os.rmdir(temp_img_dir)
        
    except Exception as e:
        print(f"Error processing PDF to videos: {str(e)}")

def process_all_to_videos():
    """
    Process all PDFs and their corresponding audio files into videos
    """
    pdf_dir = "PDF"
    audio_dir = "audio"
    video_dir = "Short-Form-Videos"
    
    if not os.path.exists(pdf_dir):
        print("PDF directory not found.")
        return
    if not os.path.exists(audio_dir):
        print("Audio directory not found. Please create audio files first.")
        return
    
    os.makedirs(video_dir, exist_ok=True)
    
    pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    for pdf_file in pdfs:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        pdf_name = Path(pdf_file).stem
        
        # Check if corresponding audio directory exists
        if os.path.exists(os.path.join(audio_dir, pdf_name)):
            print(f"\nProcessing {pdf_file} to create videos...")
            process_pdf_to_videos(pdf_path, audio_dir, video_dir)
        else:
            print(f"No audio files found for {pdf_file}. Skipping...")

def process_all_transcripts():
    """
    Process all transcript files in the Transcripts directory and create videos
    """
    transcripts_dir = "Transcripts"
    if not os.path.exists(transcripts_dir):
        print("No transcripts directory found.")
        return

    print("\nStep 1: Processing transcripts to create audio files...")
    
    transcript_files = [f for f in os.listdir(transcripts_dir) if f.endswith('.txt')]
    if not transcript_files:
        print("No transcript files found in the Transcripts directory.")
        return

    for transcript_file in transcript_files:
        transcript_path = os.path.join(transcripts_dir, transcript_file)
        create_audio_from_transcript(transcript_path)
    
    print("\nStep 2: Creating videos from PDF pages and audio...")
    process_all_to_videos()

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
        print("\nVideo files have been created in the 'Short-Form-Videos' directory")
        
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
        print("5. Create Audio and Videos (from existing transcripts)")
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
            process_all_transcripts()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()