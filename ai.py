import requests
import PyPDF2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your API token as an environment variable for security
API_KEY = os.getenv("OPENAI_API_KEY")

# API endpoint for OpenAI's GPT-3.5/4 turbo model
API_URL = "https://api.openai.com/v1/chat/completions"

# Headers for the API request
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Query OpenAI's GPT-3.5/4 API
def query(prompt):
    data = {
        "model": "gpt-3.5-turbo",  # Change to "gpt-4" if you have access to GPT-4
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}],
        "max_tokens": 500
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_from_multiple_pdf(pdf_folder):
    pdf_dict = {}
    for pdf in os.listdir(pdf_folder):
        pdf_path = os.path.join(pdf_folder, pdf)
        pdf_name = os.path.splitext(pdf)[0]  # Extract file name without extension
        pdf_dict[pdf_name] = extract_text_from_pdf(pdf_path)
    return pdf_dict

term_def_generic_prompt = "I'm going to provide you with the content of a PDF document. Please analyze this content and create term-definition pairs that could be used for studying. Follow these guidelines: 1. Separate each term and its definition with an @ symbol. 2. Separate each pair with a \\ symbol. 3. If a term has multiple examples or sub-components, create a separate pair for the main term and another for its examples. 4. For the examples pair, use the format 'Term Examples@Example 1, Example 2, Example 3'. 5. Create individual pairs for each example or sub-component with its own definition. 6. Ensure that you capture all relevant information from the PDF, including main concepts, sub-concepts, examples, and explanations. 7. Keep the definitions concise but informative."

# Example usage
def key_definition_pairs(pdf_dict):
    term_def_pairs = {}
    for pdf_lecture in pdf_dict:
        
        #Testing with limited input to avoid API call limits
        
        #limited_input = pdf_dict[pdf_lecture][:100]
        #combined_input = f"{term_def_generic_prompt} {limited_input}"
        combined_input = f"{term_def_generic_prompt} {pdf_dict[pdf_lecture]}"
        
        # Request to OpenAI API
        output = query(combined_input)
        
        print(f"API Response for {pdf_lecture}:")
        print(output)
        
        if 'choices' in output and len(output['choices']) > 0:
            term_def_pairs[pdf_lecture] = output['choices'][0]['message']['content']
        else:
            print(f"Unexpected API response structure for {pdf_lecture}")
            term_def_pairs[pdf_lecture] = "Error: Unable to generate term-definition pairs"
    
    return term_def_pairs

def write_dict_to_file(dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for key, value in dictionary.items():
            file.write(f"{key}: {value}\n\n\n")

def main():
    pdf_folder = "PDF"
    set_title = "Auto-generated Lecture Flashcards"
    
    lecture_text = extract_from_multiple_pdf(pdf_folder)
    term_definition_pairs = key_definition_pairs(lecture_text)

    write_dict_to_file(term_definition_pairs, "pairs.txt")

if __name__ == "__main__":
    main()
