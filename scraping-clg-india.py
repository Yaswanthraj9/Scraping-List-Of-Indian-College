# The requests library
from inspect import Parameter
from multiprocessing.dummy import Value
from lxml.etree import fromstring
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import base64
import time
  
sum=0
clg_india_url=[]
for i in range(0,1000):
    url="{"+'"url"'+":"+'"india-colleges"'+","+'"page"'+":"+str(i)+"}"
    url_bytes = url.encode("ascii")
    base64_bytes = base64.b64encode(url_bytes)
    base64_string = base64_bytes.decode("ascii")
    clg_india_url.append('https://collegedunia.com/web-api/listing?data='+base64_string)


header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

parameter=[]

def clg_web(parameter_item,id):
    url="https://collegedunia.com/university/"+str(id)
    try:
        page=requests.get(url,headers=header)
        doc=BeautifulSoup(page.text, 'lxml')
        list=['co','cs','c','cd']
        for item in list:
            try:
                table=doc.find('h2',{'id':item}).find_next_sibling('div',{'class':'table-responsive'})
                parameter_item["List_of_Courses"]=pd.read_html(str(table))[0].to_dict(orient = 'records')
            except:
                continue
    except:
        pass

def clg_placement(parameter_item,id):
    url="https://collegedunia.com/university/"+str(id)+"/placement"
    try:
        page=requests.get(url,headers=header)
        doc=BeautifulSoup(page.text, 'lxml')
        table=doc.find('table')
        parameter_item["Placement"]=pd.read_html(str(table))[0].to_dict(orient = 'records')
    except:
        pass

def clg_cutoff(parameter_item,id):
    url="https://collegedunia.com/university/"+str(id)+"/cutoff"
    try:
        page=requests.get(url,headers=header)
        doc=BeautifulSoup(page.text, 'lxml')
        table=doc.find('table')
        parameter_item["Cut_Off"]=pd.read_html(str(table))[0].to_dict(orient = 'records')
    except:
        pass

for val in range(0,len(clg_india_url)):
    #request= requests.get(clg_india_url)
    try:
        page=requests.get(clg_india_url[val],headers=header)
        doc = BeautifulSoup(page.text, 'lxml')
        clg_name = doc.find_all('pre')

        dict_clg=json.loads(page.text)

        for i in range(0,len(dict_clg["colleges"])):
            time.sleep(10)
            parameter_item={}
            data=dict_clg["colleges"][i]
            print(data["college_name"])
            parameter_item["College Name"]=data["college_name"]
            parameter_item["College City"]=data["college_city"]
            parameter_item["State"]=data["state"]
            parameter_item["Approvals"]=data["approvals"]
            clg_web(parameter_item,data["college_id"])
            clg_placement(parameter_item,data["college_id"])
            clg_cutoff(parameter_item,data["college_id"])
            sum+=1
            parameter.append(parameter_item)

        if (val+1)%10==0:
            top_colleges_df=pd.DataFrame(parameter)
            top_colleges_df.to_csv('top_clgs_new.csv', index=None)
            df_new = pd.read_csv('top_clgs_new.csv')
            GFG = pd.ExcelWriter('top_clgs_new.xlsx')
            df_new.to_excel(GFG, index=False)
            GFG.save()
    except:
        print("error")
        print(clg_india_url[val])
        val-=1
        time.sleep(1200)
print(sum)

top_colleges_df=pd.DataFrame(parameter)
top_colleges_df.to_csv('top_clgs_new_all.csv', index=None)
df_new = pd.read_csv('top_clgs_new_all.csv')
GFG = pd.ExcelWriter('top_clgs_new_all.xlsx')
df_new.to_excel(GFG, index=False)
GFG.save()