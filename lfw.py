#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
"""
@Author  : zhoutao
@License : (C) Copyright 2013-2017, China University of Petroleum
@Contact : zhoutao@s.upc.edu.cn
@Software: PyCharm
@File    : lfw.py
@Time    : 2019/6/18 16:59 
@Desc    : 
"""

import numpy as np
import config as cfg
import os


class LFW(object):
    def __init__(self, data):
        self.model_path = cfg.model_path
        # 初始化参数
        self.k = cfg.factor
        self.data = data
        # 获取评分矩阵
        self.matrix = data.matrix
        # 归一化矩阵
        # self.normal()
        # 获取用户矩阵
        self.users = list(data.users)
        # 获取房间矩阵
        self.rooms = list(data.rooms)
        # 计算出矩阵的行与列数
        self.num_user = self.matrix.shape[0]
        self.num_item = self.matrix.shape[1]
        # 初始化因子矩阵
        self.P = np.mat(np.random.normal(0, 1, [self.num_user, self.k]))
        self.Q = np.mat(np.random.normal(0, 1, [self.k, self.num_item]))
        # 将评分矩阵中非零的值变为1，形成新矩阵
        self.loc = np.array(self.matrix)
        self.loc[self.loc >= 1] = 1

        model = os.path.join(self.model_path, "model.npz")
        if os.path.exists(model):
            self.load()
        self.train(step=3000)
        pass

    def update(self):
        self.data.update_data()
        # 获取评分矩阵
        self.matrix = self.data.matrix
        # 归一化矩阵
        self.normal()
        # 获取用户矩阵
        self.users = list(self.data.users)
        # 获取房间矩阵
        self.rooms = list(self.data.rooms)
        # 计算出矩阵的行与列数
        self.num_user = self.matrix.shape[0]
        self.num_item = self.matrix.shape[1]
        # 初始化因子矩阵
        self.P = np.mat(np.random.normal(0, 1, [self.num_user, self.k]))
        self.Q = np.mat(np.random.normal(0, 1, [self.k, self.num_item]))
        # 将评分矩阵中非零的值变为1，形成新矩阵
        self.loc = np.array(self.matrix)
        self.loc[self.loc >= 1] = 1
        self.train()
        pass

    def normal(self):
        """
        归一化输入矩阵
        :return:
        """
        # 获取最大值
        max_value = np.max(self.matrix)
        min_value = np.min(self.matrix)
        # 归一化
        self.matrix = (self.matrix - np.tile(min_value, self.matrix.shape)) / np.tile(max_value - min_value, self.matrix.shape)
        # 去除Nan
        self.matrix = np.nan_to_num(self.matrix)
        pass

    def loss(self):
        """
        计算出损失函数的值
        :return: loss损失函数值
        """
        tmp = self.matrix - np.array(self.P * self.Q)
        loss = np.sum(np.square(self.loc * tmp)) / 2
        return loss
        pass

    def train(self, alpha=0.01, lama=0.01, step=1000):
        """
        采用随机梯度下降方法求最优解
        :param alpha: 学习率
        :param lama: 正则化系数
        :param step: 训练步长
        :return:
        """
        for i in range(step):
            loss = self.loss()
            # print("[train] loss: {}".format(loss))
            if loss < 0.01:
                self.save_data()
                print("training is end")
                break
            tmp = self.P * self.Q - np.mat(self.matrix)
            dP = -1.0 * alpha * np.multiply(np.mat(self.loc), tmp) * self.Q.T - lama * self.P
            dQ = -1.0 * alpha * self.P.T * np.multiply(np.mat(self.loc), tmp) - lama * self.Q
            grad_p = np.array(dP)
            grad_q = np.array(dQ)
            self.P += grad_p
            self.Q += grad_q
        self.pred = np.array(np.mat(self.P) * np.mat(self.Q))
        self.save_data()
        pass

    def save_data(self):
        # 预测结果
        model = os.path.join(self.model_path, "model.npz")
        np.savez(model, self.P, self.Q, self.pred, P=self.P, Q=self.Q, predict=self.pred)
        pass

    def load(self):
        model = os.path.join(self.model_path, "model.npz")
        result = np.load(model, allow_pickle=True)
        self.P = np.mat(result["P"])
        self.Q = np.mat(result["Q"])
        self.pred = result["predict"]
        pass

    def predict(self, userId, k):
        if userId not in self.users:
            raise Exception("用户不存在")
        index = self.users.index(userId)
        pred = self.pred[index]
        idx = np.argsort(pred)[::-1][0:k]
        result = []
        for id in idx:
            result.append(self.rooms[id])
        return result
    pass

