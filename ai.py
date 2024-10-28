import requests
import PyPDF2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query(prompt):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}],
        "max_tokens": 500
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_by_page(pdf_path):
    """Extract text from PDF, returning a list where each element contains text from one page"""
    page_texts = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text.strip():  # Only add non-empty pages
                page_texts.append(text)
    return page_texts

#testing the function with a single pdf slide as to not waste tokens
def create_brainrot_lecture(pdf_path):
        """Create simplified explanations for the first page of a PDF"""
        page_texts = extract_text_by_page(pdf_path)
        simplified_explanations = []
        
        brainrot_prompt = "Break this down into smaller, easier-to-understand parts.  Be concise yet thorough so include important procedures, facts, dates, formulas, or core ideas related to this topic. Also, create a memorization technique to remember these core concepts easily for example (but not limited to) using analogies and real-life examples to simplify the concept and make it more relatable. Also dont respond with any human remarks like SURE HERE IS YOUR ANSWER, just give me the text i am requesting. Also dont use asterisks to bold text, dont try to change text formatting in that manner. You can use dashes to separate ideas though. Here's the content to explain: "

        #trendy_brainrot_prompt = "Break this down into smaller, easier-to-understand parts.  Be concise yet thorough so include important procedures, facts, dates, formulas, or core ideas related to this topic. Also, create a memorization technique to remember these core concepts easily for example (but not limited to) using analogies and real-life examples to simplify the concept and make it more relatable, however, what ever technique you use, you must phrase it in tiktok brainrot ways. Also dont respond with any human remarks like SURE HERE IS YOUR ANSWR, just give me the text i am requesting. Here's the content to explain: "
       
        if page_texts:
            print(f"Processing page 5 of {len(page_texts)}...")
            response = query(brainrot_prompt + page_texts[5])
            
            if 'choices' in response and len(response['choices']) > 0:
                explanation = response['choices'][0]['message']['content']
                simplified_explanations.append(explanation)
            else:
                simplified_explanations.append("Error processing page 5")
        
        return simplified_explanations

def process_all_pdfs_brainrot(pdf_folder):
    """Process all PDFs in the folder for brainrot lectures"""
    # Create Transcripts folder if it doesn't exist
    transcripts_folder = "Transcripts"
    if not os.path.exists(transcripts_folder):
        os.makedirs(transcripts_folder)

    for pdf in os.listdir(pdf_folder):
        if pdf.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf)
            pdf_name = os.path.splitext(pdf)[0]  # Get filename without extension
            
            print(f"\nProcessing {pdf}...")
            explanations = create_brainrot_lecture(pdf_path)
            
            # Create individual transcript file
            output_file = os.path.join(transcripts_folder, f"{pdf_name}.txt")
            write_single_transcript(pdf_name, explanations, output_file)
            print(f"Created transcript file: {output_file}")

def write_single_transcript(pdf_name, explanations, output_file):
    """Write explanations for a single PDF to its own file"""
    with open(output_file, 'w', encoding='utf-8') as file:
        #file.write(f"BRAINROT LECTURE: {pdf_name}\n")
        #file.write(f"{'='*50}\n\n")
        
        for page_num, explanation in enumerate(explanations, 1):
            if explanation != "Skipped for testing":  # Only write non-skipped pages
                file.write(f"\nPAGE {page_num}:\n")
                file.write(f"{'-'*20}\n")
                file.write(f"{explanation}\n")
                file.write(f"{'-'*20}\n")

def extract_from_multiple_pdf(pdf_folder):
    pdf_dict = {}
    for pdf in os.listdir(pdf_folder):
        if pdf.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf)
            pdf_name = os.path.splitext(pdf)[0]
            pdf_dict[pdf_name] = extract_text_from_pdf(pdf_path)
    return pdf_dict

term_def_generic_prompt = "I'm going to provide you with the content of a PDF document. Please analyze this content and create term-definition pairs that could be used for studying. Follow these guidelines: 1. Separate each term and its definition with an @ symbol. 2. Separate each pair with a \\ symbol. 3. If a term has multiple examples or sub-components, create a separate pair for the main term and another for its examples. 4. For the examples pair, use the format 'Term Examples@Example 1, Example 2, Example 3'. 5. Create individual pairs for each example or sub-component with its own definition. 6. Ensure that you capture all relevant information from the PDF, including main concepts, sub-concepts, examples, and explanations. 7. Keep the definitions concise but informative."

def key_definition_pairs(pdf_dict):
    term_def_pairs = {}
    for pdf_lecture in pdf_dict:
        combined_input = f"{term_def_generic_prompt} {pdf_dict[pdf_lecture]}"
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

'''
#testing the function with a single pdf slide as to not waste tokens
def create_brainrot_lecture(pdf_path):
        """Create simplified explanations for the first page of a PDF"""
        page_texts = extract_text_by_page(pdf_path)
        simplified_explanations = []
        
        brainrot_prompt = "Break this down into smaller, easier-to-understand parts.  Be concise yet thorough so include important procedures, facts, dates, formulas, or core ideas related to this topic. Also, create a memorization technique to remember these core concepts easily for example (but not limited to) using analogies and real-life examples to simplify the concept and make it more relatable. Also dont respond with any human remarks like SURE HERE IS YOUR ANSWR, just give me the text i am requesting. Here's the content to explain: "
        #brainrot_prompt_v2 = "Break this down into smaller, easier-to-understand parts.  Be concise yet thorough so include important procedures, facts, dates, formulas, or core ideas related to this topic. Also, create a memorization technique to remember these core concepts easily for example (but not limited to) using analogies and real-life examples to simplify the concept and make it more relatable. Also dont respond with any human remarks like SURE HERE IS YOUR ANSWER, just give me the text i am requesting. Also dont use asterisks to bold text, dont try to change text formatting in that manner. You can use dashes to separate ideas though. Here's the content to explain: "

        #trendy_brainrot_prompt = "Break this down into smaller, easier-to-understand parts.  Be concise yet thorough so include important procedures, facts, dates, formulas, or core ideas related to this topic. Also, create a memorization technique to remember these core concepts easily for example (but not limited to) using analogies and real-life examples to simplify the concept and make it more relatable, however, what ever technique you use, you must phrase it in tiktok brainrot ways. Also dont respond with any human remarks like SURE HERE IS YOUR ANSWR, just give me the text i am requesting. Here's the content to explain: "
       
        if page_texts:
            print(f"Processing page 5 of {len(page_texts)}...")
            response = query(brainrot_prompt + page_texts[5])
            
            if 'choices' in response and len(response['choices']) > 0:
                explanation = response['choices'][0]['message']['content']
                simplified_explanations.append(explanation)
            else:
                simplified_explanations.append("Error processing page 5")
        
        return simplified_explanations


def create_brainrot_lecture(pdf_path):
    """Create simplified explanations for each page of a PDF"""
    page_texts = extract_text_by_page(pdf_path)
    simplified_explanations = []
    
    brainrot_prompt = "Break this down into smaller, easier-to-understand parts.  Be concise yet thorough so include important procedures, facts, dates, formulas, or core ideas related to this topic. Also, create a memorization technique to remember these core concepts easily for example (but not limited to) using analogies and real-life examples to simplify the concept and make it more relatable. Also dont respond with any human remarks like SURE HERE IS YOUR ANSWR, just give me the text i am requesting. Here's the content to explain: "
    #brainrot_prompt_v2 = "Break this down into smaller, easier-to-understand parts.  Be concise yet thorough so include important procedures, facts, dates, formulas, or core ideas related to this topic. Also, create a memorization technique to remember these core concepts easily for example (but not limited to) using analogies and real-life examples to simplify the concept and make it more relatable. Also dont respond with any human remarks like SURE HERE IS YOUR ANSWER, just give me the text i am requesting. Also dont use asterisks to bold text, dont try to change text formatting in that manner. You can use dashes to separate ideas though. Here's the content to explain: "

    for page_num, page_text in enumerate(page_texts, 1):
        print(f"Processing page {page_num} of {len(page_texts)}...")
        response = query(brainrot_prompt + page_text)
        
        if 'choices' in response and len(response['choices']) > 0:
            explanation = response['choices'][0]['message']['content']
            simplified_explanations.append(explanation)
        else:
            simplified_explanations.append(f"Error processing page {page_num}")
    
    return simplified_explanations
'''