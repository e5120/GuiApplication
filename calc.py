# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class Calc():
    def __init__(self):
        self.fname = []
        self.arr = []
        self.material = []

    # ファイル追加
    def addFile(self, filename):
        self.fname.append(filename)
        self.arr.append(pd.read_csv(self.fname[-1], header=None, delimiter="\t"))
        # カラム登録
        self.arr[-1].columns = ["path", "eval1", "eval2", "judge"]

        self.material.append((self.processing(self.arr[-1])))
        return self.material

    # ファイルの内容を整理
    def processing(self, arr):
        img_sum = np.size(arr["judge"])
        # 危険、安全と判断した写真の数
        djudge_sum = np.size(np.where(arr["judge"] == 1))
        sjudge_sum = np.size(np.where(arr["judge"] == 2))

        # 危険、安全として与えた写真の数
        arr["path"].str.extract("(safe)")
        arr["path"].fillna("danger")
        dimg_sum = np.size(np.where(arr["path"].str.extract("(danger)") == "danger"))
        simg_sum = np.size(np.where(arr["path"].str.extract("(safe)") == "safe"))

        # AIの判定と人間の判定が一致した数
        dmatch_sum = np.size(np.where((arr["path"].str.extract("(danger)") == "danger") & (arr["judge"] == 1)))
        smatch_sum = np.size(np.where((arr["path"].str.extract("(safe)") == "safe") & (arr["judge"] == 2)))

        dmatch_rate = dmatch_sum / dimg_sum * 100
        smatch_rate = smatch_sum / simg_sum * 100

        return [["danger", dimg_sum, djudge_sum, dmatch_sum, dmatch_rate], ["safe", simg_sum, sjudge_sum, smatch_sum,  smatch_rate], img_sum]
