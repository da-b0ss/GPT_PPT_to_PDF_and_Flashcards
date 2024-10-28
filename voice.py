from gtts import gTTS
import pyttsx3
import os
from pathlib import Path

def convert_text_to_mp3_gtts(input_file, output_file=None, lang='en', accent='com'):
    """
    Convert text file to MP3 using Google Text-to-Speech (better quality, no speed control).
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
        
    if output_file is None:
        output_file = input_path.with_suffix('.mp3')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='latin-1') as file:
            text = file.read()
    
    print(f"Converting text to speech using Google TTS...")
    tts = gTTS(text=text, lang=lang, tld=accent)
    
    print(f"Saving MP3 to: {output_file}")
    tts.save(str(output_file))
    
    return str(output_file)

def convert_text_to_mp3_pyttsx3(input_file, output_file=None, rate=200, voice_id=None):
    """
    Convert text file to MP3 using pyttsx3 (speed control available).
    
    Args:
        input_file (str): Path to input text file
        output_file (str, optional): Path for output MP3 file
        rate (int): Speech rate (default: 200)
                   - Normal speed is around 200
                   - Range typically: 50 (very slow) to 400 (very fast)
        voice_id (str, optional): Specific voice to use
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
        
    if output_file is None:
        output_file = input_path.with_suffix('.mp3')
    
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Set the speech rate
    engine.setProperty('rate', rate)
    
    # Set voice if specified
    if voice_id:
        engine.setProperty('voice', voice_id)
    
    # Read the text file
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='latin-1') as file:
            text = file.read()
    
    print(f"Converting text to speech using pyttsx3...")
    print(f"Speech rate: {rate}")
    
    # Save as MP3
    print(f"Saving MP3 to: {output_file}")
    engine.save_to_file(text, str(output_file))
    engine.runAndWait()
    
    return str(output_file)

def list_available_voices():
    """List all available voices with their IDs."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print("\nAvailable voices:")
    for idx, voice in enumerate(voices):
        print(f"{idx + 1}. ID: {voice.id}")
        print(f"   Name: {voice.name}")
        print(f"   Languages: {voice.languages}")
        print(f"   Gender: {voice.gender}")
        print()
    
    return voices

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert text file to MP3 with speech rate control')
    parser.add_argument('input_file', help='Path to input text file')
    parser.add_argument('--output', '-o', help='Path to output MP3 file (optional)')
    parser.add_argument('--engine', '-e', choices=['gtts', 'pyttsx3'], default='pyttsx3',
                      help='Speech engine to use (default: pyttsx3)')
    parser.add_argument('--rate', '-r', type=int, default=200,
                      help='Speech rate (50-400, default: 200) - only works with pyttsx3')
    parser.add_argument('--language', '-l', default='en',
                      help='Language code for gTTS (default: en)')
    parser.add_argument('--accent', '-a', default='com',
                      help='Accent TLD for gTTS (com=US, co.uk=British, etc.)')
    parser.add_argument('--list-voices', action='store_true',
                      help='List available voices and exit')
    parser.add_argument('--voice-id', help='Specific voice ID to use with pyttsx3')
    
    args = parser.parse_args()
    
    if args.list_voices:
        list_available_voices()
        exit()
    
    try:
        if args.engine == 'gtts':
            output_path = convert_text_to_mp3_gtts(
                args.input_file,
                args.output,
                args.language,
                args.accent
            )
        else:  # pyttsx3
            output_path = convert_text_to_mp3_pyttsx3(
                args.input_file,
                args.output,
                args.rate,
                args.voice_id
            )
        
        print(f"Conversion completed successfully!")
        print(f"Output saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")