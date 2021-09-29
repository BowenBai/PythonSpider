# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 22:35:28 2021

@author: 10043
"""
import geopandas as gpd
import requests
import numpy as np


dict_data ={"jinxing.json":"禁行点分布"}

Name = "bbw"
sampleNo = 1000
# 一维正态分布
# 下面三种方式是等效的
mu = 3
sigma = 0.1
np.random.seed(0)
s = np.random.normal(mu, sigma, sampleNo )

for key in dict_data:
    print(key)
    url = "http://henan.tianditu.gov.cn/zhoukou/szzt/jinxing.json"
    data = requests.get(url)
    print(data.text)
    gdata = gpd.read_file(data.text)
    # if(len(gdata) >= 1):
    #     gdata.to_file(dict_data[key]+".shp" ,crs=4326 , encoding = 'gb18030')