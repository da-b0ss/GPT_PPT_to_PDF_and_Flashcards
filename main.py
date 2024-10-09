import comtypes.client
import os
import sys

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
        
        # Set custom export options based on the image
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

        # Try exporting with each option individually to identify any problematic parameters
        for key, value in export_options.items():
            try:
                if key == "Path":
                    continue  # Skip Path as it's required
                temp_options = {"Path": output_file_name, "FixedFormatType": 2, key: value}
                deck.ExportAsFixedFormat(**temp_options)
                print(f"Successfully exported with {key}")
            except Exception as e:
                print(f"Error with parameter {key}: {str(e)}")

        # Now try with all options
        try:
            deck.ExportAsFixedFormat(**export_options)
            print(f"Successfully converted {input_file_name} to {output_file_name} with custom settings")
        except Exception as e:
            print(f"Error during final export: {str(e)}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        try:
            deck.Close()
        except:
            pass
        powerpoint.Quit()

def ppt_to_pdf(input_file_name, output_file_name):
    # Get absolute paths
    input_file_name = os.path.abspath(input_file_name)
    output_file_name = os.path.abspath(output_file_name)

    # Check if input file exists
    if not os.path.exists(input_file_name):
        raise FileNotFoundError(f"Input file not found: {input_file_name}")

    # Ensure output file has .pdf extension
    if not output_file_name.lower().endswith('.pdf'):
        output_file_name += ".pdf"

    # Prompt user for export method
    while True:
        choice = input("Choose export method:\n1. Default\n2. Custom (with settings from image)\nEnter 1 or 2: ")
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    if choice == '1':
        ppt_to_pdf_default(input_file_name, output_file_name)
    else:
        ppt_to_pdf_custom(input_file_name, output_file_name)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'test.pptx')
    output_file = os.path.join(script_dir, 'lecture.pdf')
    
    ppt_to_pdf(input_file, output_file)