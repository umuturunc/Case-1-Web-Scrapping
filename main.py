from bs4 import BeautifulSoup
import urllib
import json

link = "https://finans.mynet.com/borsa/hisseler/"
f = urllib.request.urlopen(link) #url'yi aç
html_doc = f.read() #web sayfasını içeriğini oku
soup = BeautifulSoup(html_doc, 'html.parser')   #html içeriğini ağaç benzeri bir veri yapısına dönüştür
hisselerResultSet = soup.findAll(class_="mr-4") #Hisseler, mr-4 class ismine sahip taglarda bulunur
hisselerDictionary = dict()
hisselerHrefs = []  #Her bir hissenin kendi sayfasının URL'sinin tutulduğu dizi
for result in hisselerResultSet:
    href = result.find("a").get("href")
    hisselerHrefs.append(href)
    a=href.split('/')
    hisseAdi = href.split("/")[5] + "/"
    hisselerDictionary[hisseAdi] = ""

print(type(hisselerHrefs[0])) 
for hisseLink in hisselerHrefs:    
    print(hisseLink)
    f = urllib.request.urlopen(hisseLink)   #hisse bilgilerinin olduğu URL'yi aç
    html_doc = f.read() #açılan sayfayı oku
    soup = BeautifulSoup(html_doc, 'html.parser')   #okunan sayfayı BeautifulSoup veri yapısına dönüştür
    attributesResultSet = soup.findAll(class_="flex align-items-center justify-content-between")
    #Hisseye ait bütün attribute'leri oku
    hisseAttributesDictionary = dict()
    #hissenin attribute anahtar ve değerlerinin tutulduğu dictionary
    for result in attributesResultSet:
        #attribute listesi içindeki her bir attribute için
        print(result)
        spans = result.findAll("span")
        print(spans)
        key = spans[0].text
        value = spans[1].text
        print(key + value)
        hisseAttributesDictionary[key] = value
    hisseAdi = hisseLink.split("/")[5] + "/"
    value = hisseAttributesDictionary
    hisselerDictionary[hisseAdi] = value
    
print(hisselerDictionary)

#verileri json dosyasına yazdır
with open('mynet.json', 'w', encoding='utf-8') as f:
    json.dump(hisselerDictionary, f, ensure_ascii=False, indent=4)

#çekilen verileri mongodb'ye yazma
from pymongo import MongoClient
#localhost:27017'de çalışan mongodb bağlantısı
client = MongoClient('localhost', port=27017)
#mynet-database adında veritabanı oluşturuluyor
db = client["mynet-database"]
#jsondata adında tablo oluşturuluyor
col = db["jsondata"]
#siteden çekilip dictionary veri yapısında tutulan veriler bir satıra ekleniyor
result = db.jsondata.insert_one(data)
