import requests
from bs4 import BeautifulSoup
import pickle
import time

#header 부분은 봇이 아니고 사용자라는 것을 알리기 위해 입력 

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'}
b=[]
c=[]
d=''
for x in range(1,31+1):
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page="+str(x)
    print(url)
    data = requests.get(url,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    time.sleep(0.1)
    title = str(soup.select('.tltle'))
    #print(title)
    a = title.split(',')
    #print(a)

    KOSDAQ={}
    i=0

    for i in range(0,len(a)):
        b.append(a[i][46:52])
        #repr()lace 함수를 이용해 중간 공백 제거]
       
        d=a[i][54:-4].replace("<","").replace(" ","")
        c.append(d)
        
        i = i+1
    #print(b)
for y in range(0,len(b)):
    KOSDAQ[c[y]]=b[y]

print(KOSDAQ)
    

f = open('/workspace/20210511/FINANCE/LIST_PROJECT/DBandDB_SOURCE/KOSDAQ.txt', 'ab')
pickle.dump(KOSDAQ, f)
f.close()



