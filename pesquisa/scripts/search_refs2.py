import pdfplumber, os

files = os.listdir(".")
geron = next((f for f in files if "ron" in f and f.endswith(".pdf") and "Survey" not in f and f != "book.pdf" and f != "normas_fatec_2022_artigo.pdf"), None)
survey = "A_Survey_of_Ensemble_Learning_Concepts_Algorithms_Applications_and_Prospects.pdf"

def read_pages(filename, page_list, max_chars=2500):
    with pdfplumber.open(filename) as pdf:
        for pi in page_list:
            if pi >= len(pdf.pages): continue
            try:
                txt = pdf.pages[pi].extract_text() or ""
                print(f"\n--- PAGE {pi+1} ---")
                print(txt[:max_chars])
            except Exception as e:
                print(f"Page {pi+1}: SKIP ({e})")

# Géron: instance-based learning section (around p.18-22 = pages 28-32 in PDF)
print("=== GERON: Instance-based & lazy learning ===")
read_pages(geron, [27, 28, 29, 30, 31])

# Géron: feature scaling (pages 72-75 = PDF pages ~82-85)
print("\n=== GERON: Feature Scaling ===")
read_pages(geron, [80, 81, 82, 83, 84])

# Géron: cross-validation (pages 76-78 = PDF pages ~86-88)
print("\n=== GERON: Cross-Validation ===")
read_pages(geron, [85, 86, 87, 88, 100, 101])

# Géron: confusion matrix, precision, recall (ch3)
print("\n=== GERON: Confusion Matrix / Precision / Recall ===")
read_pages(geron, [99, 100, 101, 102, 103, 104])

# Survey: KNN mention
print("\n\n=== SURVEY: KNN pages ===")
with pdfplumber.open(survey) as pdf:
    hits = []
    for i, page in enumerate(pdf.pages):
        try:
            txt = page.extract_text() or ""
        except:
            txt = ""
        if any(k.lower() in txt.lower() for k in ["nearest neighbor", "knn", "k-nearest"]):
            hits.append(i)
    print(f"KNN pages in survey: {hits}")
    for pi in hits[:6]:
        try:
            txt = pdf.pages[pi].extract_text() or ""
            print(f"\n--- SURVEY PAGE {pi+1} ---")
            print(txt[:2500])
        except Exception as e:
            print(f"Page {pi+1}: {e}")

# book.pdf: normalization/similarity pages (ch7 = around pages 88-94)
print("\n\n=== BOOK.PDF: Similarity & Normalization (ch7) ===")
read_pages("book.pdf", [87, 88, 89, 90, 91, 92, 93, 94])
