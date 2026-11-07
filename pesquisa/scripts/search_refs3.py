import pdfplumber, os

files = os.listdir(".")
geron = next((f for f in files if "ron" in f and f.endswith(".pdf") and "Survey" not in f and f != "book.pdf" and f != "normas_fatec_2022_artigo.pdf"), None)
survey = "A_Survey_of_Ensemble_Learning_Concepts_Algorithms_Applications_and_Prospects.pdf"

# Try reading pages with encoding errors using latin-1 fallback
def read_page_safe(page):
    """Try multiple extraction methods."""
    for method in [
        lambda p: p.extract_text(),
        lambda p: p.extract_text(x_tolerance=5, y_tolerance=5),
    ]:
        try:
            return method(page) or ""
        except:
            pass
    # Try raw words
    try:
        words = page.extract_words()
        return " ".join(w["text"] for w in words)
    except:
        return ""

print("=== GERON: Instance-based / lazy learning (PDF pages 28-35) ===")
with pdfplumber.open(geron) as pdf:
    for pi in range(27, 37):
        txt = read_page_safe(pdf.pages[pi])
        if txt.strip():
            print(f"\n--- PAGE {pi+1} ---")
            print(txt[:2500])

print("\n\n=== GERON: Feature Scaling (PDF pages 80-86) ===")
with pdfplumber.open(geron) as pdf:
    for pi in range(79, 87):
        txt = read_page_safe(pdf.pages[pi])
        if txt.strip():
            print(f"\n--- PAGE {pi+1} ---")
            print(txt[:2500])

print("\n\n=== GERON: Cross-Validation (PDF pages 85-92, ch2) ===")
with pdfplumber.open(geron) as pdf:
    for pi in range(84, 92):
        txt = read_page_safe(pdf.pages[pi])
        if txt.strip():
            print(f"\n--- PAGE {pi+1} ---")
            print(txt[:2000])

print("\n\n=== SURVEY: stability / KNN / bagging pages 2-6 ===")
with pdfplumber.open(survey) as pdf:
    for pi in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        txt = read_page_safe(pdf.pages[pi])
        if txt.strip() and any(k in txt.lower() for k in ["nearest", "knn", "stable", "bagging", "heart"]):
            print(f"\n--- SURVEY PAGE {pi+1} ---")
            print(txt[:3000])

print("\n\n=== BOOK.PDF: chapter 7, normalization / distances (pages 88-100) ===")
with pdfplumber.open("book.pdf") as pdf:
    for pi in range(87, 100):
        txt = read_page_safe(pdf.pages[pi])
        if txt.strip():
            print(f"\n--- BOOK PAGE {pi+1} ---")
            print(txt[:2500])
