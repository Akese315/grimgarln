import io
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def extract_text_from_page(pdf_path, page_number):
    output_string = io.StringIO()
    resource_manager = PDFResourceManager()
    laparams = LAParams()
    codec = 'utf-8'
    device = TextConverter(resource_manager, output_string,codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)

    with open(pdf_path, 'rb') as file:
        for page in PDFPage.get_pages(file, [page_number],check_extractable=True):
            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                    if hasattr(element, 'fontname'):
                        font = element.fontname
                    else:
                        font = 'Unknown Font'

                    text = element.get_text().strip()
                    if text:
                        is_text_bold = is_bold(font)
                        print("Text:", text)
                        print("Is Bold:", is_text_bold)
                        print("---")

    text = output_string.getvalue()
    device.close()
    output_string.close()
    return text

def regexFun(matched):
    valeur = ""
    if matched.group(1) is None:
        valeur = " »" [::-1]  + matched.group(0)
    else:
        valeur = " » \n" [::-1]  + matched.group(0)
    return  valeur


text = extract_text_from_page("volume/1/Volume.pdf", 39)

text = re.sub(r'\n+', '\n', text)

matchesSTART = re.finditer(r'[—«]', text)
matchesEND = re.finditer(r'[»]', text)


indicesSTART = [m.start(0) for m in matchesSTART]

indicesEND = [m.start(0) for m in matchesEND]


position = 0

for i in range(len(indicesSTART)):
    result = ""
    new_result = ""

    if  position < indicesSTART[i]  :
        print(text[position:indicesSTART[i]])
        position = indicesSTART[i] +1


    for indexEND in indicesEND:
        if i+1 < len(indicesSTART):
            if indexEND > indicesSTART[i+1]:
                result = text[indicesSTART[i]:indicesSTART[i+1]]
                new_result = result.replace("—","«")
                new_result = re.sub(r'([!?.…])+\s*(\n)?',regexFun, new_result[::-1], count=1)[::-1]
                position = indicesSTART[i+1] +1
                print(new_result, end = '')
                #input("")
                break
        if indicesSTART[i] < indexEND :
            result = text[indicesSTART[i]:indexEND]
            new_result = result.replace("—","«")
            new_result = re.sub(r'([!?.…])+\s*(\n)?',regexFun, new_result[::-1], count=1)[::-1]
            position = indexEND +1
            print(new_result, end = '')
            #input("")
            break
    
if position > indicesSTART[len(indicesSTART)-1]:
    print(text[position:(len(text)-1)])



