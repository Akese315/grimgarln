import fitz
import PyPDF2
import re
regex = r"(CHAPITRE +)?([0-9]+)+ *[:.] *.*"
regex2 = r"CHAPITRE\s+(\d+)\s*:"
regex3 = r"([0-9]+)\s*[:.]\s*(\w+)"
regexLevel = r"(Niveau)\s*[0-9]+\s*[:.]\s*(\w+)"
masterGodSupremeRegex = r"(?:\s+|\n)[—«\"]\s*((?:(?:(?:[^»\"!](?!\n—)*)(?:[?!])*)(?!(?:(?:\n+—)|(?:\n+«))))*)"
masterGodSupremeRegex2 = r"(?!\s+|\n)[—«\"]\s*((?:(?:(?:[^»\"!](?!\n—)*)(?:[?!])*)(?!(?:(?:\n+—)|(?:\n+«))))*)"



vol = int(input("quel est le volume"))


def extract_chapter(vol):
    pdf_path = 'volume/' + str(vol) + '/Volume.pdf'
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        chapters_page = []
        current_chapter = 0
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text = page.extract_text()
            header  = []
            header.append(text.split("\n")[0])
            for j in range(1,3):
                if j >= len(text.split("\n")):
                    break
                text1= text.split("\n")[-j]
                text2= text.split("\n")[j]
                header.append(text1)
                header.append(text2)
            
            for j in range(len(header)):
                match = re.search(regex2, header[j])
                match2 = re.search(regex3, header[j])
                Level = re.search(regexLevel, header[j])
                chapter= 0
                if Level:
                    continue
                if match:
                    chapter =int(match.group(1))
                elif match2:
                    chapter =int(match2.group(1))
                if current_chapter < chapter:
                    current_chapter = chapter
                    chapters_page.append(i) 
        return chapters_page

def extract_text(page):
    content=""   
    speeches= extract_speech(page)
    styles : list= extract_style(page)
    text = page.get_text("text")
    nspeech = 0
    nstyle = 0


    for i in range(len(text)):
        if text[i] == '\n':
            content+= "<br>"
            continue
        if nspeech != len(speeches) and i == speeches[nspeech]["start"]:
            content+="<span class='speech'>"
        if nstyle != len(styles) and i == styles[nstyle]["start"]:
            content+="<span class='"+ styles[nstyle]["style"]+"'>"
        content+= text[i]

        if nstyle != len(styles) and i == styles[nstyle]["end"]:
            content+= "</span>"
            nstyle+=1
        if nspeech != len(speeches) and i == speeches[nspeech]["end"]:
            content+= "</span>"
            nspeech+=1

    return {"content": content , "page" : None}
   
def extract_style(page):
    BOLD = 2 ** 4
    ITALIC = 2 **1
    styles= []
    position = 0
    blocks = page.get_text("dict", flags=11)["blocks"]
    for element in blocks:
        for l in element["lines"]:
            if l == None:
                continue
            for s in l["spans"]:
                if s["flags"] & BOLD:
                    styles.append({"start" : position, "end": (len(s['text'])-1), "style" : "bold" })
                if s["flags"] & ITALIC:
                     styles.append({"start" : position, "end": (len(s['text'])-1), "style" : "italic" })
                position += len(s['text'])
    return styles


def extract_speech(page):
    speeches = []
    text = page.get_text("text")
    matches =re.finditer(masterGodSupremeRegex, text,flags=re.MULTILINE)
    for match in matches:
        position = match.span(1)
        speeches.append({"start": position[0], "end" : position[1]})
    return speeches

    
def extract_image(page):
    page.get_images()

def create_img_tag(src):
    img_tag = "<img src='" + src+ "'/>"
    
def create_span_tag(content, style):
    p_tag = "<span style=' font-family : " + style['font']+"; font-style: "+style['mode']+";' >"+content+"</span>"
    return p_tag


def createChapters(vol, chapters : list):
    pdf_path = 'volume/' + str(vol) + '/Volume.pdf'
    doc = fitz.open(pdf_path)
    file = None
    for i in range(len(chapters)-1):
        print("from page ", chapters[i], "to page ", chapters[i+1])
        pages = doc[chapters[i]:chapters[i+1]]
        full_content =""
        for page in pages:
            full_content+=extract_text(page)["content"]
        path = "volume/"+ str(vol) + "/chapitre_" +  str(i+1)+ '.html'
        file =  open(path, "w")
        file.write(full_content)
        file.close()
        print("done")
    doc.close()

chapters = extract_chapter(vol)
createChapters(vol,chapters)

#chapters = extract_chapter(vol)
#createChapters2(3,chapters)
#print(chapters)

#createChapters2(vol)
