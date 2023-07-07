import fitz
import re

regex = r"(CHAPITRE +)?([0-9]+)+ *[:.] *.*"


vol = int(input("quelle est le volume"))


'''
def extract_text(page):
    text = page.get_text("blocks")
    formattedText = list()
    for element in text: 

        indicesStart = re.finditer(r'[—«]', element)
        indicesEnd = re.finditer(r'[»]', element)
        formattedText.append({'str':element[0:indicesStart[0]]})
        for index in indicesStart:
            if len(indicesEnd) > 0:
                formattedText.append({'str': element[indicesStart[index]:indicesEnd[0]]})
                indicesEnd.pop(0)
'''
        
def extract_text(page):
    content = ""
    numero_chapitre = 0
    blocks = page.get_text("dict", flags=11)["blocks"]
    if len(blocks) > 0 and "lines" in blocks[0]:
        match = re.search(regex, blocks[0]['lines'][0]['spans'][0]['text'])
        if match:
            numero_chapitre = int(match.group(2))  
            blocks[0]['lines'][0]['spans'].pop(0)
           
    for element in blocks:
        for l in element["lines"]:
            for s in l["spans"]:
                tag = ""
                if s["flags"] & 2 ** 1:
                    tag = create_span_tag(s["text"], {'mode':"italic", 'font': s["font"]})
                else:
                    tag = s["text"]
                content +=tag
            content += "<br>"
            #print(content)
    return {'text' : "<p style=' font-family : TimesNewRomanPS-ItalicMT;' >" + content + "</p>", 'chap' : numero_chapitre}
    
   
def extract_style(page):
    print("hey")

    
def extract_image(page):
    page.get_images()

def create_img_tag(src):
    img_tag = "<img src='" + src+ "'/>"
    
def create_span_tag(content, style):
    p_tag = "<span style=' font-family : " + style['font']+"; font-style: "+style['mode']+";' >"+content+"</span>"
    return p_tag
    


# Example usage


pdf_path = 'volume/' + str(vol) + '/Volume.pdf'
doc = fitz.open(pdf_path)

chapNum = -1
path = "volume/"+ str(vol) + "/chapitre_" +  str(chapNum)+ '.html'
file = None
for i in range(doc.page_count):
    text = extract_text(doc[i])
    if text['chap'] > chapNum:
        chapNum = text['chap']
        path = "volume/"+ str(vol) + "/chapitre_" +  str(chapNum)+ '.html'
        if file is not None:
            file.close()
        file =  open(path, "w")
        print(chapNum)   
    file.write(text['text'])
    #print(text['text'], "page : ", i)
    #input()

doc.close()