import fitz
import PyPDF2
import re
regex = r"(CHAPITRE +)?([0-9]+)+ *[:.] *.*"
regex2 = r"(CHAPITRE\s+(\d+)\s*:)"
regex3 = r"(([0-9]+)\s*[:.]\s*(\w+))"
regexPage = r"<br>\s*(\d)\s*<br>"

authorRegex =r"((?:Ao Jyumonji))"
titleRegex = r"(Grimgar\w*\W*le\w*\W*monde\w*\W*de((\w?\W?)(?!de))*cendres((\w?\W?)(?!de))*et(?:\w*\W*)de\w*\W*fantaisie)"

regexLevel = r"(Niveau)\s*[0-9]+\s*[:.]\s*(\w+)"
masterGodSupremeRegex = r"(?:\s+|\n)[—«\"]\s*((?:(?:(?:[^»\"!](?!\n—)*)(?:[?!])*)(?!(?:(?:\n+—)|(?:\n+«))))*)"
masterGodSupremeRegex2 = r"(?!\s+|\n)[—«\"]\s*((?:(?:(?:[^»\"!](?!\n—)*)(?:[?!])*)(?!(?:(?:\n+—)|(?:\n+«))))*)"



vol = int(input("quel est le volume"))


def extract_chapter(vol):
    pdf_path = 'volume/' + str(vol) + '/Volume.pdf'
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        chapters_page = []
        first_chapter = True
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
                chapter= None
                if Level or ( not match2 and not match):
                    continue
                if match:
                    chapter =int(match.group(2))
                elif match2:
                    chapter =int(match2.group(2))
                if current_chapter < chapter or first_chapter:
                    current_chapter = chapter
                    first_chapter = False
                    chapters_page.append(i) 
        return chapters_page

def extract_text(page):
    content=""   
    speeches= extract_speech(page)
    styles : list= extract_style(page)
    text = page.get_text("text")
    nspeech = 0
    nstyle = 0

    for i in range(0, len(text)):
        if text[i] == '\n':
            content += "<br>"
        
        if text[i] != "\n":
            content += text[i]

        if nstyle != len(styles) and i == styles[nstyle]["end"]:
            content += "</span>"
            nstyle+=1
        if nspeech != len(speeches) and i == speeches[nspeech]["end"]:
            content += "</span>"
            nspeech +=1
        if nspeech != len(speeches) and i == speeches[nspeech]["start"]:
            content +="<span class='speech'>"
        if nstyle != len(styles) and i == styles[nstyle]["start"]:
            content +="<span class='"+ styles[nstyle]["style"]+"'>"

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
                    styles.append({"start" : position, "end": (position+len(s['text'])), "style" : "bold" })
                if s["flags"] & ITALIC:
                     styles.append({"start" : position, "end": (position+len(s['text'])), "style" : "italic" })
                position += len(s['text'])
    return styles


def extract_speech(page):
    speeches = []
    text = page.get_text("text")
    matches =re.finditer(masterGodSupremeRegex2, text,flags=re.MULTILINE)
    for match in matches:
        position = match.span(1)
        speeches.append({"start": position[0]-1, "end" : position[1]})
    return speeches

    
def extract_image(page):
    page.get_images()

def create_img_tag(src):
    img_tag = "<img src='" + src+ "'/>"

def cleanPage(text:str):
    chapterMatch = re.finditer(regex2, text, re.IGNORECASE)
    match1List = list(chapterMatch)
    

    if len(match1List) != 0:
        print(match1List[0].group(1))
        position = match1List[0].span(1)
        text = text[:position[0]] + text[position[1]:]

    match2 = re.finditer(regex3, text)
    match2List = list(match2)
    if len(match2List) != 0:
        print(match2List[0].group(1))
        position = match2List[0].span(1)
        text = text[:position[0]] + text[position[1]:]

    
    
    authorMatch = re.finditer(authorRegex,text ,re.MULTILINE)
    authorMatchList = list(authorMatch)
    if len(authorMatchList) != 0:
        position = authorMatchList[0].span(1)
        text = text[:position[0]] + text[position[1]:]
    titleMatch = re.finditer(titleRegex,text ,flags=(re.MULTILINE|re.IGNORECASE))
    titleMatchList = list(titleMatch)
    if len(titleMatchList) != 0:
        position = titleMatchList[0].span(1)
        text = text[:position[0]]+ text[position[1]:]

    
    pageMatches = re.finditer(regexPage, text)
    pageMatchesList = list(pageMatches)
    print("nombre de page", len(pageMatchesList))
    for i in range(len(pageMatchesList) - 1, -1, -1):
        position = pageMatchesList[i].span(1)
        text = text[:position[0]] + text[position[1]:]

    return text


def createChapters(vol, chapters : list):
    pdf_path = 'volume/' + str(vol) + '/Volume.pdf'
    doc = fitz.open(pdf_path)
    file = None
    for i in range(len(chapters)-1):
        print("from page ", chapters[i], "to page ", chapters[i+1])
        pages = doc[chapters[i]:chapters[i+1]]
        full_content =""
        for page in pages:
            full_content+= extract_text(page)["content"]
        full_content = cleanPage(full_content)
        path = "volume/"+ str(vol) + "/chapitre_" +  str(i)+ '.html'
        file =  open(path, "w")
        file.write(full_content)
        file.close()
        print("done")
    doc.close()
'''
pdf_path = 'volume/' + str(vol) + '/Volume.pdf'
doc = fitz.open(pdf_path)
page = doc[20]
full_content=extract_text(page)["content"]
full_content = cleanPage(full_content)
print(full_content)
'''
chapters = extract_chapter(vol)
print(chapters)
createChapters(vol,chapters)
