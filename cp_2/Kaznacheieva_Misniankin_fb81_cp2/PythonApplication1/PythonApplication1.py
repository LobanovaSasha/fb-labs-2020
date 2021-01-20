from collections import Counter
from itertools import cycle
import re
import math


key_1 = 'да'
key_2 = 'нет'
key_3 ='семь'
key_4 = 'кошка'
key_5 = 'декоммунизация'


alpha = [chr(i) for i in range(ord('а'),ord('я')+1)]


def encrypt(file,result_file, key):
    fin = open (file, "rt", encoding="utf-8")
    fout = open(result_file, "wt", encoding="utf-8")
    text = fin.read()
    print(text)
    txt=''
    n=0
    for i in range(0, len(text)):
        if text[i] in alpha:
            txt=alpha[(alpha.index(text[i])+alpha.index(key[n%len(key)]))%32]
            n+=1
            #print(n)
            fout.write(txt)
            #print (txt)

  
def decrypt(file,result_file, key):
    fin = open (file, "rt", encoding="utf-8")
    fout = open(result_file, "wt", encoding="utf-8")
    text = fin.read()
    print(text)
    dtxt=''
    n=0
    for i in range(0, len(text)):
        if text[i] in alpha:
            dtxt=alpha[(alpha.index(text[i])-alpha.index(key[n%len(key)])+len(alpha))%32]
            n+=1
           # print(n)
            fout.write(dtxt)
            #print (dtxt)


def c_ind(txt):
    
    l=len(txt)
    if l==1:
        res=1/l/l
    else:
        res=1/(l-1)/l

    freq = c_freq(txt)
    sum = 0
    for let in freq:
        sum = sum + freq[let] * (freq[let] - 1)
    c=res*sum
    return c


def c_freq(text):
    freq = {}
    c = Counter(text)
    for f in c:
        freq[f] = c[f]
    return freq



def divided(txt, block_num):
    arr = []
    for cnt in range(0, len(txt), block_num):
        arr.append(txt[cnt:cnt+block_num])
    return arr


def find_key(filename):
    fin= open (filename, "rt", encoding="utf-8")
    fulltext = fin.read()
    for i in range(2, 30):
        parttext = divided(fulltext, i)
        temp = ""
        for n in parttext:
            temp += n[0]
        sum_of_blocks = count_index(temp)
        print("i = ", i, "index = ", sum_of_blocks)

def most_freq_letter(index_list):
    max_index = 0
    indexes = index_list.values()
    for ind in indexes:
        if ind > max_index:
            max_index = ind
    return get_key(index_list, max_index)


def get_key(dict, num):
    key_list = list(dict.keys())
    val_list = list(dict.values())
    position = val_list.index(num)
    return key_list[position]

def search_key(filename, len_of_key):
    fin = open (filename, "rt", encoding="utf-8")
    fout = open('results.txt', "wt", encoding="utf-8")
    text = fin.read()
    key_list = divided(text, len_of_key)
    russian_most_used = ('о','а','е','и','т','н','с','р', 'л')
    print (russian_most_used)
    for let in russian_most_used:
        res = ""
        for k in range(0, len_of_key):
           temp = ""
           for m in key_list:
                if  k < len(m) :
                    temp += m[k]
           ll = most_freq_letter(c_freq(temp))
           key = (ord(ll) - ord(let)) % 32 + 1072
           res = res + chr(key)
           print("With ", let, "result is", res, '\n')
           fout.write(res)




#find_key('text.txt')
search_key('text.txt', 15)
#encrypt('small.txt', 'decryted.txt', key_5)
