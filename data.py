#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2017, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : data.py 
@Time    : 2019/6/19 20:22 
@Desc    : 
"""
import config as cfg
import numpy as np
import pymysql
import json
import os


class Data(object):
    def __init__(self):
        self.conn = pymysql.connect(host=cfg.host, user=cfg.username,
                    password=cfg.password,database=cfg.database, charset="UTF8")
        self.cursor = self.conn.cursor()
        self.data_path = cfg.data_path
        if os.path.exists(self.data_path + "data.npz")\
                and os.path.exists(self.data_path+"data.json"):
            self.load_data()
        pass

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_all_user_order_room(self):
        sql = "select user,room from conference;"
        # 执行查询SQL语句
        self.cursor.execute(sql)
        # 获取数据
        results = self.cursor.fetchall()
        order_room = {}
        for item in results:
            # 生成字典
            user = item[0]
            room = item[1]
            key = "{},{}".format(user,room)
            # 统计次数
            if key not in order_room:
                order_room[key] = 1
            else:
                order_room[key] += 1
            pass
        return order_room
        pass

    def get_all_room(self):
        sql = "select * from room order by roomid;"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        rooms = [result[0] for result in results]
        return rooms
        pass

    def get_all_user(self):
        sql = "select * from user order by userid;"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.user = [result[0] for result in results]
        return self.user
        pass

    def get_user_items_matrix(self):
        matrix = np.zeros([len(self.users), len(self.rooms)])
        for item in self.order_room.items():
            # 获取key
            key = item[0]
            # 切分，获取行与列的值
            row, col = key.split(",")
            # 获取下标
            i = self.users.index(int(row))
            j = self.rooms.index(int(col))
            value = item[1]
            matrix[i][j] = value
            pass
        return matrix
        pass

    def update_data(self):
        # 更新数据
        self.users = self.get_all_user()
        self.rooms = self.get_all_room()
        self.order_room = self.get_all_user_order_room()
        self.matrix = self.get_user_items_matrix()
        self.save_data()
        pass

    def save_data(self):
        data_file = os.path.join(self.data_path, "data")
        np.savez(data_file + ".npz", self.users, self.rooms,self.matrix,
                 user=self.users, room=self.rooms, data=self.matrix)
        str = json.dumps(self.order_room)
        with open(data_file + ".json", "w") as f:
            f.write(str)
        print("成功")
        pass

    def load_data(self):
        data_file = os.path.join(self.data_path, "data")
        data = np.load(data_file + ".npz", allow_pickle=True)
        self.users = data["user"]
        self.rooms = data["room"]
        self.matrix = data["data"]
        with open(data_file+".json") as f:
            self.order_room = json.load(f)
        print("加载数据成功")
        pass
