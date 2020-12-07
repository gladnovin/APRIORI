#!/usr/bin/python
import sys
from collections import defaultdict
from collections import Counter
import pandas as pd
car =pd.read_csv("Play_Tennis_Data_Set.csv")

def data():
    return car.values
    
   
def firstpass(car):
    candidate =[]
    for t in c:
        for im in t:
            if not [im] in candidate:
                candidate.append([im])
    return list(map(frozenset,sorted(candidate)))


def traverse(l, ci, mins):
    o = defaultdict(int)
    for t1 in l:
        for item in ci:
            if item.issubset(t1):
                if not item in o:
                    o[item]= 1
                else:
                    o[item] +=1
    total = float(len(l))
    flist = []
    frequent = defaultdict(int)
    for k in o:
        s = o[k]/total
        if s >= mins:
            flist.insert(0,k)
        frequent[k] = s
    return flist,frequent


def execute(c,mins,minc):
    c=data()
    candidate=firstpass(c)
    l=list(map(set,c))
    f1,frequent=traverse(l,candidate,mins)
    f=[f1]
    p=2
    while (len(f[p-2]) > 0):
        ci=pair(f[p-2],p)
        candidate1,frequent1=traverse(l,ci,mins)
        frequent.update(frequent1)
        f.append(candidate1)
        p +=1
    association(f,frequent,minc)
    return f,frequent
  
def pair(candidate1,p):
    flist =[]
    for i in range(0,len(candidate1)):
        m=sorted(list(candidate1[i]))[0:p-2]
        for j in range(i+1,len(candidate1)):
            m1=sorted(list(candidate1[j]))[0:p-2]
            if m == m1:
                flist.append(candidate1[i].union(candidate1[j]))
    return flist

def con(recset,d,frequent,y,minc):
    split=[]
    for c1 in d:
        e=frequent[recset]/frequent[recset-c1]
        confidence=e
        if confidence >= minc:
            print(recset-c1,'=>',c1,'confidence:',confidence)
            recsetstr = str(recset-c1)
            c1str = str(c1)
            confidencestr = str(confidence)
            f.write(recsetstr + "=>" + c1str +" , " + "confidence" + " "+ confidencestr)
            y.extend((recset-c1,c1,confidence))
            split.append(c1)
    return split

def rc(recset,d,frequent,y,minc):
    b=len(d[0])
    if (len(recset)>(b+1)):
        gen=pair(d,b+1)
        gen=con(recset,gen,frequent,y,minc)
        if(len(gen)>1):
            rc(recset,gen,frequent,y, minc)
def association(f,frequent,minc):
    valid=[]
    for i in range(1,len(f)):
        for recset in f[i]:
            d=[frozenset([im]) for im in recset]
            if(i>1):
                rc(recset,d,frequent,valid,minc)
            else:
                con(recset,d,frequent,valid,minc)
    return valid


c=data()
f=open('Rules.txt',"a+")
mins=input("enter the minsupport")
x1=str(mins)
f.write(x1)
minc=input("enter the confidence")
x2=str(minc)
print(execute(c,mins,minc))
h1=str(execute(c,mins,minc))
f.write(h1)
f.close()



