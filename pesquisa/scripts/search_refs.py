import pdfplumber, os

def read_pages(filename, page_list, max_chars=2000):
    with pdfplumber.open(filename) as pdf:
        for pi in page_list:
            if pi >= len(pdf.pages):
                continue
            try:
                txt = pdf.pages[pi].extract_text() or ""
                print(f"\n--- PAGE {pi+1} ---")
                print(txt[:max_chars])
            except Exception as e:
                print(f"Page {pi+1}: {e}")

def search_pages(filename, keywords):
    hits = []
    with pdfplumber.open(filename) as pdf:
        for i, page in enumerate(pdf.pages):
            try:
                txt = page.extract_text() or ""
            except:
                txt = ""
            for kw in keywords:
                if kw.lower() in txt.lower():
                    hits.append(i)
                    break
    return hits

files = os.listdir(".")
geron = next((f for f in files if "ron" in f and f.endswith(".pdf") and "Survey" not in f and f != "book.pdf" and f != "normas_fatec_2022_artigo.pdf"), None)
survey = next((f for f in files if "Survey" in f), None)

print(f"Géron file: {geron}")
print(f"Survey file: {survey}")

# Search Géron for KNN
print("\n\n=== GERON - KNN pages ===")
hits = search_pages(geron, ["k-nearest", "nearest neighbor", "knn", "instance-based"])
print(f"Hit pages (0-indexed): {hits[:20]}")

# Read relevant pages from Géron (instance-based and KNN)
print("\n=== GERON pages around KNN ===")
read_pages(geron, hits[:6], max_chars=2500)

# Géron cross-validation pages
print("\n\n=== GERON - cross-validation pages ===")
hits_cv = search_pages(geron, ["cross-validation", "cross_val_score", "stratifiedkfold"])
print(f"CV hit pages: {hits_cv[:15]}")
read_pages(geron, hits_cv[:3], max_chars=2000)

# Géron feature scaling
print("\n\n=== GERON - Feature scaling pages ===")
hits_scale = search_pages(geron, ["standardization", "z-score", "StandardScaler", "feature scaling"])
print(f"Scaling hit pages: {hits_scale[:10]}")
read_pages(geron, hits_scale[:2], max_chars=2000)
