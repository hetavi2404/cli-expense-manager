from sentence_transformers import SentenceTransformer, util
from pdfminer.high_level import extract_text
import os

# --- Load model ---
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- Extract and split PDF into paragraphs ---
def extract_paragraphs(pdf_path):
    text = extract_text(pdf_path)
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 30]
    return paragraphs

# --- Embed all paragraphs ---
def embed_paragraphs(paragraphs):
    return model.encode(paragraphs, convert_to_tensor=True)

# --- Search similar content ---
def search(query, embeddings, paragraphs, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_results = scores.argsort(descending=True)[:top_k]

    for i, idx in enumerate(top_results):
        print(f"\n--- Match {i+1} (Score: {scores[idx]:.4f}) ---\n{paragraphs[idx]}")

# --- MAIN ---
if __name__ == "__main__":
    pdf_file = "pdfs/imp.pdf"  # Change this to your file path

    print("🔍 Extracting content...")
    paragraphs = extract_paragraphs(pdf_file)
    print(f"✅ Extracted {len(paragraphs)} paragraphs.")

    print("🔗 Generating embeddings...")
    embeddings = embed_paragraphs(paragraphs)

    while True:
        query = input("\n🧠 Enter your semantic search query (or 'exit'): ")
        if query.lower() == 'exit':
            break
        search(query, embeddings, paragraphs)

# testing "extracting paragraphs"
# if __name__ == "__main__":
#     paragraphs = extract_paragraphs("pdfs/imp.pdf")
#     print(f"Found {len(paragraphs)} paragraphs.")
#     print(paragraphs[:3])  # print first 3
