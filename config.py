#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2017, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : config.py 
@Time    : 2019/6/19 20:24 
@Desc    : 
"""

# [Data]
# 数据库配置
host = "*.*.*.*."
username = "*"
password = "****"
database = "***"
# 数据存放位置
data_path = "./data/"

# [Train]
# 模型存放位置
model_path = "./model/"
# 潜在因子数
factor = 4


# [predict]
# 推荐数目
topN = 5
