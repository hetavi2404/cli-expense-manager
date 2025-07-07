import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer, util
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer as SumyTokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Setup
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, good balance

# --- Text Processing Functions ---
def extract_pdf_text(path):
    return extract_text(path)

def clean_tokens(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    return [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def summarize_text(text, sentence_count=5):
    parser = PlaintextParser.from_string(text, SumyTokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def split_into_paragraphs(text):
    return [para.strip() for para in text.split("\n") if len(para.strip()) > 30]

def embed_paragraphs(paragraphs):
    return model.encode(paragraphs, convert_to_tensor=True)

def semantic_search(query, paragraphs, embeddings, top_k=3):
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, embeddings, top_k=top_k)[0]
    return [(paragraphs[hit['corpus_id']], hit['score']) for hit in hits]

# --- MAIN ---
if __name__ == "__main__":
    pdf_path = "pdfs/imp.pdf"

    print("📥 Extracting text...")
    raw_text = extract_pdf_text(pdf_path)

    print("🧹 Cleaned Tokens:")
    tokens = clean_tokens(raw_text)
    print(tokens[:50])

    print("🧠 Named Entities:")
    for ent, label in extract_entities(raw_text):
        print(f"{ent} → {label}")

    print("📝 Summary:")
    print(summarize_text(raw_text, sentence_count=7))

    # Prepare paragraphs for semantic search
    paragraphs = split_into_paragraphs(raw_text)
    print(f"\n📄 {len(paragraphs)} paragraphs ready for semantic search")

    embeddings = embed_paragraphs(paragraphs)

    while True:
        query = input("\n🔍 Ask something (or type 'exit'): ")
        if query.lower() == "exit":
            break
        results = semantic_search(query, paragraphs, embeddings)
        print("\n🎯 Top Matches:")
        for para, score in results:
            print(f"\n→ Score: {score:.4f}\n{para}")
