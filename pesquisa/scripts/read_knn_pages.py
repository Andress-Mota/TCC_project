import pdfplumber

# Read pages 125-135 of book.pdf (KNN section)
with pdfplumber.open("book.pdf") as pdf:
    for i in range(124, 135):
        if i >= len(pdf.pages):
            break
        try:
            txt = pdf.pages[i].extract_text()
            if txt:
                print(f"\n--- PAGE {i+1} ---")
                print(txt)
        except Exception as e:
            print(f"Page {i+1}: encoding error - {e}")
            # try with different settings
            try:
                txt = pdf.pages[i].extract_text(x_tolerance=3, y_tolerance=3)
                if txt:
                    print(f"\n--- PAGE {i+1} (alt) ---")
                    print(txt)
            except:
                pass
