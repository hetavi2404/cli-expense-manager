# summarize_pdf_local3.py

import fitz  # PyMuPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from fpdf import FPDF
import sys

# --- Extract text from PDF ---
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = "\n".join([page.get_text() for page in doc])
    return full_text

# --- Local Summarizer using sumy ---
def summarize_text(text, sentence_count=10):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return "\n".join(str(sentence) for sentence in summary)

# --- Save summary to new PDF ---
def save_summary_to_pdf(summary_text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 10, line.encode('latin-1', 'ignore').decode('latin-1'))
    pdf.output(output_path)
    print(f"\n✅ Summary saved as: {output_path}")

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize_pdf_local3.py <path_to_pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    text = extract_text_from_pdf(input_pdf)
    summary = summarize_text(text, sentence_count=15)  # You can tweak sentence count
    save_summary_to_pdf(summary, "PDF_SUMMARY_LOCAL3.pdf")

