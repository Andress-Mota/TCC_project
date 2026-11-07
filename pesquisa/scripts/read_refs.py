import pdfplumber, sys

files = [
    ("book.pdf", 8),
    ("A_Survey_of_Ensemble_Learning_Concepts_Algorithms_Applications_and_Prospects.pdf", 6),
    ("Aurelien-Geron-Hands-On-Machine-Learning-with-Scikit-Learn-Keras-and-Tensorflow_-Concepts-Tools-and-Techniques-to-Build-Intelligent-Systems-OReilly-Media-2019.pdf", 6),
]

import os
for name, npages in files:
    # find actual filename
    for f in os.listdir("."):
        if "Survey" in name and "Survey" in f:
            name = f; break
        if "Aurelien" in name and "Géron" in f:
            name = f; break
        if name == "book.pdf" and f == "book.pdf":
            break

    print(f"\n{'='*60}")
    print(f"FILE: {name}")
    print('='*60)
    try:
        with pdfplumber.open(name) as pdf:
            print(f"Total pages: {len(pdf.pages)}")
            for i, p in enumerate(pdf.pages[:npages]):
                txt = p.extract_text()
                if txt:
                    print(f"\n--- PAGE {i+1} ---")
                    print(txt[:1500])
    except Exception as e:
        print(f"ERROR: {e}")
