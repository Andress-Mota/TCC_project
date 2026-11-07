import pdfplumber, re, sys

def search_pdf(filename, keywords, pages_context=2, max_hits=8):
    print(f"\n{'='*70}")
    print(f"SEARCHING: {filename}")
    print(f"KEYWORDS: {keywords}")
    print('='*70)
    try:
        with pdfplumber.open(filename) as pdf:
            total = len(pdf.pages)
            hits = []
            for i, page in enumerate(pdf.pages):
                try:
                    txt = page.extract_text() or ""
                except:
                    txt = ""
                for kw in keywords:
                    if kw.lower() in txt.lower():
                        hits.append(i)
                        break
            print(f"Total pages: {total}  |  Hits on pages: {hits[:30]}")
            shown = 0
            for pi in hits[:max_hits]:
                start = max(0, pi - 1)
                end = min(total, pi + pages_context)
                for j in range(start, end):
                    try:
                        txt = pdf.pages[j].extract_text() or ""
                    except:
                        txt = ""
                    if txt.strip():
                        print(f"\n--- PAGE {j+1} (hit near p.{pi+1}) ---")
                        print(txt[:2000])
                shown += 1
                if shown >= max_hits:
                    break
    except Exception as e:
        print(f"ERROR: {e}")

# Search KNN sections in each book
import os
files = os.listdir(".")

geron = next((f for f in files if "G" in f and "ron" in f and f.endswith(".pdf")), None)
survey = next((f for f in files if "Survey" in f), None)
book   = "book.pdf"

# Book.pdf - find KNN chapter
search_pdf(book, ["nearest neighbor", "k-nearest", "KNN", "lazy"], max_hits=5)
