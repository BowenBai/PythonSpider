# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 22:35:28 2021

@author: 10043
"""
import geopandas as gpd
import requests

dict_data ={"jishuiqu.json":"积水点分布",
            "jinxing.json":"禁行点分布",
            "tingdian.json":"停电区分布",
            "zhongyu.json":"中雨模拟水淹范围",
            "baoyu.json":"暴雨模拟水淹范围",
            "tedabaoyu.json":"特大暴雨模拟水淹范围",
            "liangtiantedabaoyu.json":"两天特大暴雨模拟水淹范围"
            }
for key in dict_data:
    print(key)
    url = "http://henan.tianditu.gov.cn/anyang/szzt/"+key
    data = requests.get(url)
    print(data.text)
    gdata = gpd.read_file(data.text)
    if(len(gdata) >= 1):
        gdata.to_file(dict_data[key]+".shp" ,crs=4326 , encoding = 'gb18030')