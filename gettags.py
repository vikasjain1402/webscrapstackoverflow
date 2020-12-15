from bs4 import BeautifulSoup
from  json import loads,dumps
import os,time,datetime,concurrent.futures,requests

def getdata(pageno)    :
    finaldata=dict()
    url=f"https://stackoverflow.com/tags?page={pageno}&tab=popular"
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    data=soup.find_all('div',class_="s-card js-tag-cell grid fd-column")
    for i in data:
        data2=i.find_all('a',class_="post-tag")
        data3=i.find_all('div',class_="mt-auto grid jc-space-between fs-caption fc-black-400")
        data4=data3[0].find_all("div",class_="grid--cell")
        data5=i.find_all('div',class_="grid--cell fc-medium mb12 v-truncate4")
     
        finaldata[str(data2[0].text)]={"count":int(data4[0].text.split(" ")[0]),"discription":str(data5[0].text)}
    return finaldata
t1=time.perf_counter()




returnvalue=[]
with concurrent.futures.ThreadPoolExecutor() as executor:
    for i in range(1,21):
        future=executor.submit(getdata,i)
        returnvalue.append(future.result())

t2=time.perf_counter()

print("time taken: ",t2-t1)

json_object=dumps(returnvalue,indent=4)
filename=os.path.join(os.path.dirname(__file__),"tags1.json")
with open (filename,"w") as fp:
    fp.write(json_object)
