import comtypes.client
import os
import time

def ppt_to_pdf(input_file_name, output_file_name):
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
        # Try to set visibility to False, but don't raise an error if it fails
        try:
            powerpoint.Visible = False
        except:
            pass

        deck = powerpoint.Presentations.Open(input_file_name)
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
        # Allow some time for PowerPoint to close
        time.sleep(1)

def batch_convert_pptx_to_pdf(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pptx_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pptx')]

    for pptx_file in pptx_files:
        input_path = os.path.join(input_dir, pptx_file)
        output_path = os.path.join(output_dir, os.path.splitext(pptx_file)[0] + '.pdf')
        ppt_to_pdf(input_path, output_path)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lectures_dir = os.path.join(script_dir, 'Lectures')
    converted_dir = os.path.join(script_dir, 'Converted')

    batch_convert_pptx_to_pdf(lectures_dir, converted_dir)