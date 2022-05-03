"""
Invoice generator (Main Program)
"""
import os
import math
import locale
import time 

import replace_field
import json_token_generator
import word_generator

from docx2pdf import convert


# ----------------------

def main():
    """ ... """
    vinit = 0
    num_bills = 5000-vinit
    ddir = "bills//data//"
    tmpl_dir = "bills//templates//"
    print("Starting...")

    templates = [
        "template1_EndesaXXI" ,
        "template2_Iberdrola",
        "template3_GasNatural", 
        "template4_EndesaLuz", 
        "template5_Iberdrola",
        "template6_Naturgy",
        "template7_Repsol",
        "template8_EDP",
        "template9"
        ]  

    print(templates)

    for tmp in templates:
        datadir = ddir + tmp
        if not os.path.exists(datadir):
           os.makedirs(datadir)
    
    json_n=0
    json_time=0
    doc_time=0
    doc_n=0
    pdf_time=0
    pdf_n=0

    total_time=time.time()

    for tmp in templates:
        datadir = ddir + tmp
        invoice_prefix = datadir + '//Invoice'

        print("\n\n" + str(tmp) + "\n\n")

        numdigits = 4

        locale.setlocale(locale.LC_TIME, '')

        for i in range(num_bills):
            k = vinit + i + 1
            digit_file = str(k).zfill(numdigits)
            file_prefix = invoice_prefix + digit_file
            
            print(k);

            json_fn = file_prefix + '.json'
            
            print("Replacing json fields...")
            t=time.time()
            replace_field.gen_json(json_fn)
            t=time.time()-t
            json_time=json_time+t
            json_n=json_n+1

            tmpl_filename = tmpl_dir + tmp + ".docx"
            pdf_fn = file_prefix + '.pdf'

            print("Generating word and pdf files from json...")
            doc_t, pdf_t = word_generator.gen_pdf(json_fn, tmpl_filename, pdf_fn)
            doc_time += doc_t
            pdf_time += pdf_t
            doc_n=doc_n+1
            pdf_n=pdf_n+1

            # Tokens generation
            #tokenizer_json_fn = invoice_prefix + digit_file + '_token.json'
            tokenizer_json_fn = file_prefix + '_token.json'

            print("Token json generator...")    
            json_token_generator.create(json_fn, tokenizer_json_fn)

            # PDF with tokens
            pdf_fn = file_prefix + '_ann.pdf'        
    
            print("Generating word and pdf files from token json...")
            doc_t, pdf_t = word_generator.gen_pdf(tokenizer_json_fn, tmpl_filename, pdf_fn)
            doc_time += doc_t
            pdf_time += pdf_t
            doc_n=doc_n+1
            pdf_n=pdf_n+1

	
    total_time=time.time()-total_time

    print(num_bills, " facturas")

    print("Tiempo total simulación:", json_time)
    print("Timepo medio simulación:", json_time/json_n)

    print("Tiempo total generación invoice:", doc_time)
    print("Timepo medio generación invoice:", doc_time/doc_n)
    
    print("Tiempo total generación pdf:", pdf_time)
    print("Timepo medio generación pdf:", pdf_time/pdf_n)
 
    print("Tiempo total:", total_time)
    print("Timepo medio:", total_time/(num_bills*len(templates)))
    print("Tiempo medio por factura:", json_time/json_n + 2*doc_time/doc_n + 2*pdf_time/pdf_n)


if __name__ == '__main__':
    main()
