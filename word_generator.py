"""
  Word template generator
"""
import os
import json
from docx2pdf import convert
from docxtpl import DocxTemplate
import time

def gen_pdf(json_fn, tmpl_filename, pdf_fn):
    """ This function creates the invoice file in PDF format """
    doc_t=time.time()
    doc = DocxTemplate(tmpl_filename)

    print("  - Reading json...")
    with open(json_fn, encoding="utf-8") as json_file:
        data = json.load(json_file)

    print("  - Reandering doc...")
    doc.render(data)

    print("  - Saving doc...")
    tmp_docx = pdf_fn+".docx"
    doc.save(tmp_docx)
    
    doc_t=time.time()-doc_t    

    # export to PDF
    pdf_t=time.time()
    print("  - Converting doc to pdf...")
    convert(tmp_docx, pdf_fn, keep_active=True)
    pdf_t=time.time()-pdf_t

    return doc_t, pdf_t
