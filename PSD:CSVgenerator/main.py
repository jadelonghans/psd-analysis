"""By CHINEN AND DANGOL"""

#coding:utf-8
from scipy import signal
import wave
import numpy as np
import csv
import math

def wavread(filename):
    wf = wave.open(filename, "r")
    fs = wf.getframerate()
    x = wf.readframes(wf.getnframes())
    x = np.frombuffer(x, dtype="int16") / 32768.0  # (-1, 1)normalize
    wf.close()
    return x, float(fs)

def lowpass(wav,f):
    #print(len(f))
    k = 0

    #5KHz以上のデータを切り捨てる
    for i in range(len(f)):
        if f[i] > 5000:
            k = i
            break
    if k == 0:
        return wav,f

    #カット
    wav = wav[0:k]
    f = f[0:k]
    #print(len(f))
    return wav,f


def moving_average(data,f,n):
    #移動平均,n個の要素の平均を新たな1つの要素とする平滑化
    buff = []

    for x in xrange(len(data) - n + 1):
        y = 0.0
        for j in xrange(n):
            y += data[x + j]
        y /= n
        buff.append(y)
    #平滑化に合わせてfの要素数を調節
    f = f[ (n-1)/2 :  - (n-1)/2]
    return buff,f


def ex_moving_average(data,f,a):
    """exponential moving average"""
    # y_n = a*f_n + (1-a)*y_(n-1) という指数移動平均による平滑化
    buff = []
    y = data[0]
    data, f = lowpass(data,f)
    for i in xrange(1,len(data)):
        y = a * data[i] + (1-a) * y
        buff.append(y)
    f = f[1:len(f)]
    buff = np.array(buff)
    #print(len(f))
    #print(len(buff))
    return buff,f


def extract_peak(wave):
    a = np.array(wave)
    maxId = signal.argrelmax(a,0,3)
    return maxId[0]
 
def psd(filename):
    wav, fs = wavread(filename)
    f, Pxx_den = signal.welch(wav, fs, nperseg=1024)

    #デシベルに変換
    dbpsd = 10 * np.log10(Pxx_den)
    
    #指数移動平均
    dbpsd,f = ex_moving_average(dbpsd,f,0.5)
    #移動平均
    dbpsd ,f = moving_average(dbpsd,f,9)

    newf = f    

    #normalize
    max_f = max(f)
    dif = max_f - min (f)
    newf = (f - min (f))/dif


    peaks = extract_peak(dbpsd)

    return newf,dbpsd,peaks


if __name__ == "__main__":
    #import matplotlib.pyplot as plt
    import os

    #prepare for file writing
    with open("MYFILE.csv", "w") as f:
        c = csv.writer(f)
        c.writerow(["Name","f1","f2","f3","f4"])


        averageList = [[]] #各人に対して4つピーク情報の平均のためリストのリスト

        #set paths and names here
        paths = ["uemura_normal/",
                    "tsuchiya_normal/",
                        "fujitou_normal/"]
        names = ["uemura", "tsuchiya", "fujitou"]

        #上のディレクトリの中の各ファイルのピーク情報をCSVに書き出し、平均を計算する
        for path,name in zip(paths,names):
            data_count=0

            dirs = os.listdir( path )

            average = [0,0,0,0] #4つのピークの平均のため

            for file in dirs:
                
                print file

                if file.startswith('.'):
                    continue

                filename = path + file
                x,y,peaks = psd(filename)

                # plotting section
                # plt.plot(x,y)
                # plt.xlabel('frequency [Hz]')
                # plt.ylabel('PSD [log(V**2)/Hz]')
                # for i in peaks:
                #     plt.plot(x[i], y[i], 'bo')
                # plt.show()

                # to find out first 4 peaks
                top4 = sorted(peaks)

                #if 4 peaks are not found, fill with 1
                if len(top4) < 4:
                    for i in range(4 - len(top4)):
                        top4.append(1)

                top4 = top4[:4]

                x[1]= 1.0 #just to insert 1.0 in case above if statement occurs, does not affect graph at this point
                #目的: to enter 1.0 for values where 4 peaks are not present

                #getting actual peak positions from the indexes of x
                peakValues = [x[top4[0]],x[top4[1]],x[top4[2]],x[top4[3] ]]
                
                #csvに書き込む
                c.writerow([name,peakValues[0],peakValues[1],peakValues[2],peakValues[3]])
                
                #to calculate average
                average = [x + y for x, y in zip(average, peakValues)]
                data_count = data_count + 1

            average = [x/data_count for x in average]
            averageList.append(average)     #この人に対する平均データAverageListに追加する


        averageList = averageList[1:]       #remove the [[]] element
        print "average of each peaks for each dataset"
        print averageList