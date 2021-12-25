from bs4 import BeautifulSoup
import urllib.request as req
import requests

#수익률 함수
def rate_import(code, firstdate, lastdate,item,nowDATE):
    #봇이 아님을 증명하는 값
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'}

    try:
        firstrate=""
        lastrate=""
        for i in range(1,293+1):
            value=[]
            url="https://finance.naver.com/item/sise_day.nhn?code="+code+"&page="+str(i)
            data = requests.get(url,headers=headers)            
            soup = BeautifulSoup(data.text, 'html.parser')
            #날짜, 시세 정보 수집
            date = soup.find_all('td',attrs={'align':'center'})
            eventvalue = soup.find_all('span','tah p11')
            #필요없는 값 제거
            for i in range(0,len(eventvalue)):
                if (eventvalue[i].get_text() != "0"):
                    value.append(eventvalue[i].get_text())
                else:
                    pass
            #종료날 시세 불러오는 코드
            for i in range(1,len(date)+1):
                if(lastrate == ""):
                    DATE=date[i-1].get_text()
                    if (DATE==lastdate):
                        num = i 
                        if (num>1):
                            a=5*num-5
                            lastrate=value[a].replace(",","")
                            break
                        elif (num==1):
                            lastrate=value[num-1].replace(",","")
                            break
                        else:
                            print("오류 발생!")
                    else:
                        pass
                else:
                    pass
                num=""
            #시작날 시세 불러오는 코드
            for j in range(1,len(date)+1):
                if(firstrate == ""):
                    DATE2=date[j-1].get_text()
                    if (DATE2==firstdate):
                        num2 = j 
                        if (num2>1):
                            b=5*num2-5
                            firstrate=value[b].replace(",","")
                            break
                        elif (num2==1):
                            firstrate=value[num2-1].replace(",","")
                            break
                        else:
                            print("오류 발생!")
                    else:
                        pass
                else: 
                    pass
            #가격 모두 찾았을 때 종료
            if (firstrate!="" and lastrate!=""):
                break

        get_first = format(int(firstrate),',')
        first = "매수 지점 > "+firstdate+" : "+get_first+"원"
        get_last = format(int(lastrate),',')
        last = "매도 지점 > "+lastdate+" : "+get_last+"원"
            
        #수익률 계산
        rateprofit=(int(lastrate)-int(firstrate))/int(firstrate)*100
        profit = "수익률 : {:.2f}".format(rateprofit,',')+"%"
        print(item)
        print(first)
        print(last)
        print(profit)
        
        return profit,first,last
        
    except:
        print("알림 : <수익률 계산 중 오류가 발생했습니다.>")

#종목 저장 함수
def finance_save(nowDATE,rate):
    try:
        #해당 날짜 파일에 저장
        path="/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/FINANCE_DB/"+nowDATE+".txt"
        file = open(path, 'a')
        file.write(rate.strip())
        file.write("\n")
        file.close()
        print("알림 : <"+nowDATE+".txt 파일에 저장을 완료했습니다.>")

    except:
        print("알림 : <오류가 발생했습니다.>")


#수익률 저장 함수
def profit_save(item,first,last,profit):
    try:
        #변수에 정보 저장 후 파일에 내용 추가 
        ratereturn = item+"\n"+first+"\n"+last+"\n"+str(profit)
        longline = "--------------------------------------------------------"
        print(ratereturn)
        profitpath= "/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/"+item+".txt"
        file = open(profitpath, 'a')
        file.write(ratereturn.strip())
        file.write("\n"+longline)
        file.write("\n")
        file.close()
        print("알림 : <"+item+".txt 파일에 저장을 완료했습니다.>")
        
    except:
        print("알림 : <오류가 발생했습니다.>")

#수익률 조회한 종목 저장 함수
def save_item(item):
    try:
        path = "/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/ITEM.txt"
        file = open(path,"a")
        file.write(item.strip())
        file.write("\n")
        file.close()
    except:
        print("알림 : <수익률 조회 종목 저장 중 오류가 발생했습니다.>")
#수익률 조회한 종목 불러오는 함수
def open_item():
    try:
        path = "/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/ITEM.txt"
        file = open(path,'r')
        item = file.read().splitlines()
        file.close()
        return item
    except:
        print("알림 : <수익률 조회 종목 불러오는 중 오류가 발생했습니다.>")
#수익률 조회한 종목 초기화하는 함수
def reset_item():
    try:
        path = "/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/ITEM.txt"
        file = open(path,'w')
        file.close() 
        
    except:
        print("알림 : <수익률 조회 종목 초기화 중 오류가 발생했습니다.>")

#수익률 출력하는 함수
def open_profit(acitem):
    try:
        itempath="/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/"+acitem+".txt"
        file = open(itempath, 'r')
        content = file.read().splitlines()
        file.close()
        return content
    except:
        print("알림 : <오류가 발생했습니다.>")

#수익률 초기화
def reset_profit(openitem):
    try:
        for i in range(0,len(openitem)):
            path = "/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/"+openitem[i]+".txt"
            openfile = open(path, 'w')
            openfile.close()
    except:
        print("알림 : <수익률 초기화 중 오류가 발생했습니다.")