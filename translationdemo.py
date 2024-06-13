import fitz
import requests
import uuid
import pandas as pd
from tabulate import tabulate

# Azure Translator endpoint and subscription key
endpoint = "https://api.cognitive.myservices.com/"
subscription_key = "MyAPIKey"
location = "MyAzureLocation"

def translate_text(text, target_language):
    path = '/translate?api-version=3.0'
    params = '&to=' + target_language
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]
    
    response = requests.post(constructed_url, headers=headers, json=body)
    print(f"Translation Request Body: {body}")
    print(f"Translation Response Status Code: {response.status_code}")
    print(f"Translation Response: {response.json()}")
    response.raise_for_status()  # This will raise an error for bad responses
    return response.json()[0]['translations'][0]['text']

def extract_and_translate_pdf(file_path, target_language='ar'):
    translated_text = []
    doc = fitz.open(file_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Get all annotations
        annots = page.annots()
        if not annots:
            continue  # Skip if there are no annotations
        for annot in annots:
            text = ""
            print(f"Annotation Type: {annot.type}")
            if annot.type[0] == 8:  # Highlight annotation type
                # Extract the text from the highlighted area
                quadpoints = annot.vertices  # Get the vertices of the annotation
                x_values = [v[0] for v in quadpoints]
                y_values = [v[1] for v in quadpoints]
                x0, y0 = min(x_values), min(y_values)
                x1, y1 = max(x_values), max(y_values)
                rect = fitz.Rect(x0, y0, x1, y1)  # Create a rectangle from the quadpoints
                text += page.get_text("text", rect)
                text = text.strip()
            else:
                # For other annotation types, we will extract the annotation's content directly
                text = annot.info.get("content", "").strip()
            
            print(f"Extracted Text: {text}")
            if text:  # Ensure text is not empty
                try:
                    translated = translate_text(text, target_language)
                    translated_text.append({
                        "Page": page_num + 1,
                        "Annotation Type": annot.type,
                        "Original Text": text,
                        "Translated Text": translated
                    })
                except Exception as e:
                    print(f"Translation Error: {e}")

    return translated_text

def print_translated_elements(translated_elements):
    df = pd.DataFrame(translated_elements)
    print(tabulate(df, headers='keys', tablefmt='psql'))

# Example usage
file_path = r"C:\Data\DocumentTranslations\TheFileNameOfTheDocumentIWantTranslated.pdf"
target_language = 'ar'
translated_elements = extract_and_translate_pdf(file_path, target_language)
print_translated_elements(translated_elements)

# Use the command below in cmd to run the translationdemo app. For different languages, change the ar at the end of your command -- language codes here: https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support
# python app.py "path\file\TheFileNameOfTheDocumentIWantTranslated.pdf" ar
