import pdfplumber

with pdfplumber.open('normas_fatec_2022_artigo.pdf') as pdf:
    for i, p in enumerate(pdf.pages[:12]):
        print(f'--- PAGE {i+1} ---')
        print(p.extract_text())
        print()
