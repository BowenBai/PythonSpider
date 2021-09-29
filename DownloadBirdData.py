# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 15:33:50 2021

@author: 10043
"""
import requests
import json
import time
import pandas as pd
from pandas.io.json import json_normalize

headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
dataUrl = "http://www.birdreport.cn:8080/front/record/search/page"
reportUrl = "http://www.birdreport.cn:8080/front/record/activity/search"
def getBirdDataNew(url):
    allData = pd.DataFrame()
    for i in range(1,3): #1413552
        print(i)
        time.sleep(1)
        postdata = {"page":str(i),"limit":"10","startTime":"2001-01-01","endTime":"2021-9-3" }
        respose  = requests.post(url = dataUrl,data=postdata, headers = headers)
        
        if respose.status_code == 200:
            print("successed")
            content = respose.text
            print(content)
            json_data = json.loads(content)
            
            pd_data = json_normalize(json_data,"data")
            if len(pd_data) == 0:
                print(len(pd_data))
            pd_data.to_excel("2019_10w_" + str(i) + ".xlsx")
    
            allData.append(pd_data)
        else:
            print(respose.status_code, respose.text)
            print("Failed!!!")

    allData.to_excel("BirdData100wplus.xlsx")
    
def getReportData(url):
    allReportData = []
    for i in range(1,13):
        print(i)# 108290
        postdata = {"page":str(i),"limit":"10000","startTime":"2010-01-01","endTime":"2021-9-4" }
        respose  = requests.post(url = url,data=postdata, headers = headers)
        
        if respose.status_code == 200:
            print("successed")
            context = respose.text
            json_data = json.loads(context)
            print("="*20)
            print(json_data["count"])
            print("="*20)
            reportdata = pd.json_normalize(json_data, "data")
            print("一次请求的数据：" , len(reportdata))
            allReportData.append(reportdata)
            #allReportData.to_csv("ReportData2010_2021.csv")
            totalNum = len(allReportData)
            print("xxx",totalNum)
            #allReportData.to_csv("ReportData2010_2021.csv")
        else:
            print(respose.status_code, respose.text)
            print("Failed!!!")  
    df_allData = pd.concat(allReportData)
    df_allData.to_csv("ReportData2010_2021.csv")


getUrl = "http://www.birdreport.cn:8080/front/activity/get"
taxonUrl = "http://www.birdreport.cn:8080/front/activity/taxon"
def getBirdData(url):
    allReportData = [] ##存储所有 报告数据
    allBirdData = []  ## 存储所有 鸟类数据
    for i in range(1,12):
        print(i)# 108290
        postdata = {"page":str(i),"limit":"10000","startTime":"2010-01-01","endTime":"2021-9-4" }
        respose  = requests.post(url = url,data=postdata, headers = headers)
        if respose.status_code == 200:
            print("successed")
            context = respose.text
            json_data = json.loads(context)
            time.sleep(1)
            
            reportdata = pd.json_normalize(json_data, "data") ## DataFrame
            print(reportdata)
            report_len = len(reportdata) ##每次请求的报告数据个数
            print("一次请求的数据：" ,report_len )
            for index ,row in reportdata.iterrows() :
                activityid = row["id"]
                print("===", activityid, "===")
                getPostdata = {"activityid":activityid}
                taxonPostdata = {"activityid": activityid , "page":1, "limit": 10000} 
                get_data = requests.post(getUrl, headers = headers ,data = getPostdata)
                taxon_data = requests.post(taxonUrl, headers = headers, data = taxonPostdata) ##通过报告数据查询相应的鸟类数据
                if get_data.status_code == 200 and taxon_data.status_code == 200:
                    get_text = get_data.text
                    #print(get_text)
                    get_json_data = json.loads(get_text)
                    get_df = pd.DataFrame(get_json_data["data"], index = [0])
                    #print( type (get_df) )
                    #print(get_df)
                    taxon_text= taxon_data.text
                    taxon_json_data = json.loads(taxon_text)
                    taxon_json = pd.json_normalize(taxon_json_data, "data")
                    taxon_df = pd.DataFrame(taxon_json)
                    print(taxon_df)
                    taxon_df.to_excel("./Bird/"+ str(activityid) +"_.xlsx")
                    print("======")
                    df_result = taxon_df.join(get_df, how = "cross")
                    print(df_result) 
                    allBirdData.append(taxon_df)
                    df_result.to_excel( "./Birdplus/"+ str(activityid) +".xlsx")
                else:
                    print("Faild !!!")
            allReportData.append(reportdata)
            
            #allReportData.to_csv("ReportData2010_2021.csv")
        else:
            print(respose.status_code, respose.text)
            print("Failed!!!")  
    df_allData = pd.concat(allReportData)
    df_allData.to_csv("ReportData2010_2021.csv")
    df_allBirdData = pd.concat(allBirdData)
    df_allBirdData.to_csv("Bird.csv")
getBirdData(reportUrl)
print("Done!!!")