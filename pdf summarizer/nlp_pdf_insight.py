import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pdfminer.high_level import extract_text

# Download required resources (run once)
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# 📌 Function to extract raw text from PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# 📌 Function to tokenize and clean text
def clean_tokens(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    clean = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    return clean

# 📌 Function to perform Named Entity Recognition
def extract_named_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# 📌 MAIN
if __name__ == "__main__":
    pdf_path = "pdfs/imp.pdf"  # 🔁 change this to your own file path

    print("\n🔍 Extracting text from PDF...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("\n✅ Cleaned Tokens:")
    cleaned = clean_tokens(raw_text)
    print(cleaned[:50])  # print first 50 tokens

    print("\n🔎 Named Entities:")
    named_entities = extract_named_entities(raw_text)
    for ent, label in named_entities:
        print(f"{ent} → {label}")
