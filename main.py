import comtypes.client
import os
import sys
import subprocess

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

def get_user_choice(prompt, valid_options):
    while True:
        choice = input(prompt).lower()
        if choice in valid_options:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(valid_options)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, 'PPTX')
    output_folder = os.path.join(script_dir, 'PDF')

    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)

    # Get all user inputs upfront
    pdf_choice = get_user_choice(
        "Choose an option:\n1. Generate default PDFs\n2. Generate custom PDFs\nEnter 1 or 2: ",
        ['1', '2']
    )
    use_custom = (pdf_choice == '2')

    run_ai = get_user_choice(
        "Do you want to run the AI script (ai.py) after PDF conversion? (y/n): ",
        ['y', 'n']
    )

    # Perform PDF conversion
    print("Starting PDF conversion process...")
    process_folder(input_folder, output_folder, use_custom)
    print("PDF conversion process completed.")

    # Run AI script if requested
    if run_ai == 'y':
        print("Running AI script...")
        run_ai_script()
    else:
        print("AI script not executed.")

    print("All processes complete.")