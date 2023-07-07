import express from "express"
import http from 'http'
import cors from 'cors'
import fs from 'fs'
import path from 'path'
import pdf from "pdfjs-dist"
import history from "connect-history-api-fallback"


const viewsPath = './views/'
const app = express()


const PORT = 4000

app.get('/api/volumes', (req,res)=>
{
    var data = getNumberChapter();
    res.send(data);
})

app.get('/api/cover/:numeroVol', (req,res)=>
{
    const numeroVol = parseInt(req.params.numeroVol);
    const RelatifPath = `volume/${numeroVol}/cover.jpg`
    if (fs.existsSync(RelatifPath)) {
        res.sendFile(path.resolve(RelatifPath));
      } else {
        res.status(400).send("Bad Request");
        console.log('File does not exist.');
      }
})

app.get('/api/volumes-info=:numeroVol', (req,res)=>
{
    var numeroVol = parseInt(req.params.numeroVol);
    if(typeof(numeroVol) != "number")
    {
        res.status(400).send("Bad Request");
        return;
    }

    if(!isVolumeExists(numeroVol))
    {
        res.status(400).send("Bad Request");
        return;
    }

    res.send(listVolumeDetails(numeroVol))
});



app.get('/api/vol/:numeroVol/chap/:numeroChap', (req, res)=>
{

    var numeroVol = parseInt(req.params.numeroVol)
    var numeroChap = parseInt(req.params.numeroChap)
    
    if(typeof(numeroChap) != "number" ||  typeof(numeroVol) != "number")
    {
        console.log("not allowed")
        res.status(400).send("Bad Request");
        return;
    }
    var volumDetails = listVolumeDetails(numeroVol);
    var text = fs.readFileSync(`volume/${numeroVol}/chapitre_${numeroChap}.html`, 'utf8')
    res.send({"Text" : text})
    
})




function isVolumeExists(volNum)
{
    const dossierExiste = fs.existsSync(`volume/${volNum}`);
    if(dossierExiste)
    {
       
        return true;
    }
    return false;
}

function isChapterExists(chapNum)
{

}

function getNumberChapter()
{
    
    var data = fs.readFileSync('volume/volumes-info.json','utf-8');
    const JsonData = JSON.parse(data);
    return JsonData;
}

function listVolumeDetails(volNum)
{
    const data = JSON.parse(fs.readFileSync(`volume/${volNum}/volume-info.json`, 'utf8'));   
    return data;
        
}

async function extractTextFromPageRange(pdfPath, startPage, endPage) {
    const pdfdoc = await pdf.getDocument(pdfPath).promise;
    const numpage = pdfdoc.numPages;
    console.log(numpage);
    const page = await pdfdoc.getPage(40);
    var index = 0
    var text = await page.getTextContent();
    var items = text.items;

    var formattedText = new Array()
    var isComment = false;
    var comment = "";

    var completeText = ""

    items.forEach(element =>
        {
            completeText += element.str
        })

    console.log(completeText)

    for(var i = 0; i < items.length; i++)
    {
        var type = "normal"
        var pattern = /^g_d\d+_f1$/;
        
        if(pattern.test(items[i].fontName))
        {
            type = "italic"
        }
        // debut d'un discours
        if(items[i].str.includes("—") || items[i].str.includes("«"))
        {
            comment += items[i].str.replace("—","").replace("«","");
            if(isComment)
            {
                formattedText.push({"string" : comment, "type" : "comment"});
                comment = "";
            }
            isComment = true;
            continue;
        }

        if(items[i].str.includes("»")  || (items[i].str.includes("\n") && isComment))
        {
            comment += items[i].str.replace("»","");
            //console.log(comment+"\n")
            formattedText.push({"string" : comment, "type" : "comment"})
            isComment = false;
            comment = ""
            continue;
        }

        if(items[i].hasEOL)
        {
            formattedText.push({"string" : ' ', "type" : type})
        }

        if(isComment)
        {
            comment += items[i].str;
            continue;
        }

        

        

        formattedText.push({"string" : items[i].str, "type" : type})
        
    }

    return formattedText;
  }

  
app.use((req, res, next)=>{
    console.log(req.url)
    if (!req.originalUrl.startsWith('/api')) {
        console.log(req.url)
        history()(req, res, next);
      } else {
        console.log(req.url)
        next();
      }
});
app.use(express.static(viewsPath))
app.use(cors())
const server = http.Server(app);
  
server.listen(PORT, "localhost", () =>
{
    console.log(`Server is running on port ${PORT}.`);
});
