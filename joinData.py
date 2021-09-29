# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 23:42:24 2021

@author: 10043
"""

import pandas as pd

bird_data = pd.read_csv("D:/Workspace/GISData/Bird20210905/Bird.csv")
report_data= pd.read_csv("D:/Workspace/GISData/Bird20210905/ReportData2010_2021.csv")
report_data["activity_id"] = report_data["id"]
print(report_data)
print(bird_data.shape)
print(report_data.shape)

data = pd.merge(left = bird_data, right = report_data, how="inner", 
                left_on= "activity_id" , right_on= "id" )

print(data.shape)
print(data)
data.to_csv("MergeResult.csv")