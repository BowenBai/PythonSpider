# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 20:12:32 2021

@author: 10043
"""
import pandas as pd
import requests
import geopandas as gpd
import json
from shapely.geometry import Point


xdata = {"100":"通道通行", 
        "101":"通道通行",
        "102":"取水点",
        "105":"塌方点",
        "104":"千户停电小区",
        "103":"停水小区"}
print(xdata)

URL = 'http://henan.tianditu.gov.cn/hntdt/action/Unit/anonymous/queryUnit'
def getZaiqingData(url, metedict):
    for key in metedict.keys():
        print(key, metedict[key])
        postdata = {"cityId":"1", "isSpecialDeal": key}
        header = {"Content-Type": "application/json;charset=UTF-8",
                  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400 QQBrowser/10.8.4492.400"
                  }
        response = requests.post(url, data = json.dumps(postdata), headers = header)
        context = response.text
        print(context)
        json_data = json.loads(context)
        print(json_data)
        df_data = pd.json_normalize(json_data,"data")
        df_data.to_excel(metedict[key] + ".xlsx")
        # xx = [row for row in json_data["data"]]
        # print(xx)
        gSeier = pd.Series([ Point([ row["jd"], row["wd"] ])  for row in json_data["data"] ])
        gdf_data = gpd.GeoDataFrame(df_data, geometry= gSeier )
        gdf_data.to_file(metedict[key] + ".shp" ,crs=4326 , encoding = 'gb18030')
        
getZaiqingData(URL, xdata)