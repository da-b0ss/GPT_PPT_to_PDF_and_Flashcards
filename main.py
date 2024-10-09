import comtypes.client
import os
import time

def ppt_to_pdf(input_file_name, output_file_name, use_custom_settings=False):
    input_file_name = os.path.abspath(input_file_name)
    output_file_name = os.path.abspath(output_file_name)

    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"Input file not found: {input_file_name}")

    if not output_file_name.lower().endswith('.pdf'):
        output_file_name += ".pdf"

    powerpoint = None
    deck = None

    try:
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        try:
            powerpoint.Visible = False
        except:
            pass

        deck = powerpoint.Presentations.Open(input_file_name)
        
        if use_custom_settings:
            # Define custom settings
            custom_settings = {
                "FixedFormatType": 2,  # ppFixedFormatTypePDF
                "Intent": 1,  # ppFixedFormatIntentPrint
                "FrameSlides": True,
                "HandoutOrder": 1,  # ppPrintHorizontalFirst
                "OutputType": 1,  # ppPrintOutputSlides
                "PrintHiddenSlides": True,
                "PrintNotes": True,
                "IncludeComments": True,
                "IncludeDocProperties": True,
                "UseISO19005_1": False  # Not PDF/A compliant
            }
            
            # Apply custom settings flexibly
            try:
                deck.ExportAsFixedFormat(output_file_name, **custom_settings)
            except TypeError:
                # If too many arguments, try with fewer
                essential_settings = {
                    "FixedFormatType": 2,
                    "Intent": 1,
                    "PrintNotes": True,
                    "PrintHiddenSlides": True
                }
                deck.ExportAsFixedFormat(output_file_name, **essential_settings)
        else:
            # Export to PDF with default settings
            deck.SaveAs(output_file_name, 32)  # 32 is the format type for PDF

        print(f"Successfully converted {input_file_name} to {output_file_name}")
    except Exception as e:
        print(f"An error occurred while converting {input_file_name}: {str(e)}")
    finally:
        if deck:
            try:
                deck.Close()
            except:
                pass
        if powerpoint:
            try:
                powerpoint.Quit()
            except:
                pass
        time.sleep(1)

def batch_convert_pptx_to_pdf(input_dir, output_dir, use_custom_settings):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pptx_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pptx')]

    for pptx_file in pptx_files:
        input_path = os.path.join(input_dir, pptx_file)
        output_path = os.path.join(output_dir, os.path.splitext(pptx_file)[0] + '.pdf')
        ppt_to_pdf(input_path, output_path, use_custom_settings)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lectures_dir = os.path.join(script_dir, 'Lectures')
    converted_dir = os.path.join(script_dir, 'Converted')

    while True:
        choice = input("Do you want to use custom export settings? (y/n): ").lower()
        if choice in ['y', 'n']:
            use_custom_settings = (choice == 'y')
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    batch_convert_pptx_to_pdf(lectures_dir, converted_dir, use_custom_settings)