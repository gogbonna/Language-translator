import os
import requests
from googletrans import Translator

# Initialize Google Translate API client
translator = Translator()


# Function for Google Translate API
def google_translate(text, target_lang):
    try:
        # Detect language automatically and translate
        translation = translator.translate(text, dest=target_lang)
        print(f"Detected Language: {translation.src.upper()}")
        print(f"Google Translation to {target_lang.upper()}: {translation.text}")
        return translation.text
    except Exception as e:
        print("Error with Google Translate API:", e)
        return None


# Function for DeepL Translate API
def deepl_translate(text, target_lang):
    api_key = os.getenv('DEEPL_API_KEY',
                        'YOUR_DEEPL_API_KEY')  # Replace with your DeepL API key or set environment variable
    endpoint = "https://api-free.deepl.com/v2/translate"
    data = {
        'auth_key': api_key,
        'text': text,
        'target_lang': target_lang.upper()  # DeepL expects uppercase language codes
    }

    try:
        response = requests.post(endpoint, data=data)
        if response.status_code == 200:
            translated_text = response.json()["translations"][0]["text"]
            print(f"DeepL Translation to {target_lang.upper()}: {translated_text}")
            return translated_text
        else:
            print("DeepL API error:", response.text)
            return None
    except Exception as e:
        print("Error with DeepL API:", e)
        return None


# Main translation function with service selection
def translate_text(text, target_lang, service="google"):
    print(f"\nTranslating '{text}' to '{target_lang}' using {service.title()} API...\n")
    if service == "google":
        return google_translate(text, target_lang)
    elif service == "deepl":
        return deepl_translate(text, target_lang)
    else:
        print("Invalid service selected. Choose either 'google' or 'deepl'.")
        return None


# Program interface for user input
def main():
    text = input("Enter the text to translate: ")
    target_lang = input("Enter the target language code (e.g., 'es' for Spanish, 'fr' for French): ").strip()
    service = input("Choose translation service ('google' or 'deepl'): ").strip().lower()

    translated_text = translate_text(text, target_lang, service)
    if translated_text:
        print("\nFinal Translated Text:", translated_text)


if __name__ == "__main__":
    main()
