import comtypes.client
import os
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
if name == "main":
    script_dir = os.path.dirname(os.path.abspath(file))
    input_file = os.path.join(script_dir, 'test.pptx')
    output_file = os.path.join(script_dir, 'lecture.pdf')
   
    ppt_to_pdf(input_file, output_file)