### 4*4（それ以上でもよい4*8など）の整数データが入力されたcsvファイルを開き、次元削減を行うプログラム
### csvファイルの入力形式は以下を想定した
### F1(A) F1(B) F1(C) F1(D) ...
### F2(A) F2(B) F2(C) F2(D) ...
### ...   ...   ...   ...   ...
### F4(A) F4(B) F4(C) F4(D) ...
### このままだと行が1つの系列（一人の音声）に対応していないので扱いやすくするために転置行列にしている
### （もちろんもとの行列もそのまま残っているので使える）

import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#ファイルを開く
with open('./test.csv','r') as f:
    reader = csv.reader(f, delimiter=',')
    data = [v for v in reader] #リストにデータを格納
    
data = [[int(elm) for elm in v] for v in data] #データを数値型に変換
print(data)
Tdata = list(map(list, zip(*data))) #転置行列を生成する
print(Tdata)
#この行列か転置行列のどちらかの行が系列として扱われる（ここでは転置行列を使用）

#以下次元削減の処理
dataarray = np.array(Tdata) #元データをNumpy配列に変換

### 主成分分析による次元削減
### 参考：http://breakbee.hatenablog.jp/entry/2014/07/13/191803（ほぼそのまま）

# 共分散行列を求める
d_bar = np.array([row - np.mean(row) for row in dataarray.transpose()]).transpose()
m = np.dot(d_bar.T, d_bar) / dataarray.shape[0]
# 固有値問題を解く
(w, v) = np.linalg.eig(m)
v = v.T

# 固有値の大きい順に固有値と固有ベクトルをソート
#この部分、妥当かどうかがいまいち分からない
tmp = {}
for i, value in enumerate(w):
    tmp[value] = i

v_sorted = []
for key in sorted(tmp.keys(), reverse=True):
    v_sorted.append(v[tmp[key]])
v_sorted = np.array(v_sorted)

w_sorted = np.array(sorted(w, reverse=True))

# 次元削減
dim = 2
components = v_sorted[:dim,]
d_pca = np.dot(d_bar, components.T)

# 主成分分析終了
# そのまま部分ここまで
#print(d_pca.shape())
print(d_pca)

#グラフに描画
#方針
#1.まずデータを人ごとに分類する
#2.人ごとに色をまとめて描画する
#3.場合によってはクラスタリングを行う
plt.plot(d_pca[0][0],d_pca[0][1],"ro") #こちらの環境では描画できないが他の環境なら描画できそう
plt.plot(d_pca[1][0],d_pca[1][1],"bo")
plt.plot(d_pca[2][0],d_pca[2][1],"yo")
plt.plot(d_pca[3][0],d_pca[3][1],"ko")