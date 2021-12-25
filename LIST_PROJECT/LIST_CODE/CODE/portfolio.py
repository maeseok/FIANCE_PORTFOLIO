from bs4 import BeautifulSoup
import requests
import urllib.request as req

#현재 시세만 불러오는 함수
def present_rate(code,item,frate,number):
    try:
        #봇이 아님을 증명하는 값
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'}
        
        value=[]
        url="https://finance.naver.com/item/sise_day.nhn?code="+code+"&page=1"
        data = requests.get(url,headers=headers)            
        soup = BeautifulSoup(data.text, 'html.parser')
        #시세 정보 수집
        eventvalue = soup.find_all('span','tah p11')

        #필요없는 값 제거
        for i in range(0,len(eventvalue)):
            if (eventvalue[i].get_text() != "0"):
                value.append(eventvalue[i].get_text())
            else :
                pass                        
        firstrate=frate
        lastrate=value[0].replace(",","")
        lrate = value[0]   
        last = "현재가 : "+lrate+"원"
        rate_gap = int(lastrate) - int(firstrate)
        get_prprofit = format(rate_gap * int(number),',')
        present_profit = "현재 수익 : "+ get_prprofit+"원"
        #수익률 계산
        rateprofit= rate_gap /int(firstrate)*100
        profit = "수익률 : "+"{:0,.2f}".format(rateprofit)+"%"
        #종목 현재 손익 계산
        last_total = int(firstrate)*int(number)
        present_total = last_total + rate_gap*int(number)
        return profit,last,present_profit,present_total,last_total
    except:
        print("알림 : <현재 시세를 불러오는 중 오류가 발생했습니다.>")

#매수 정보 저장 함수
def buy_save(item, buyprice, buynumber):
    try:
        #변수에 정보 저장 후 파일에 내용 추가 
        buyreturn = item+"\n"+buyprice+"\n"+buynumber
        buypath= "/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/BUY.txt"
        file = open(buypath, 'a')
        file.write(buyreturn.strip())
        file.write("\n")
        print("알림 : <매수를 완료했습니다.>")
    except:
        print("알림 : <매수 정보 저장 중 오류가 발생했습니다.>")

#매수 정보 수정 함수
def buy_correct(item, price, number, buycollect):
    try:
        for i in range(0,len(buycollect)):
            if(buycollect[i]==item):
                #추가 매수인 경우 평단가, 수량 정보를 수정하여 리스트에 저장
                sum_first = int(buycollect[i+1])*int(buycollect[i+2])
                sum_last = int(price)*int(number)
                sum_number = int(buycollect[i+2]) + int(number)
                sum = sum_first + sum_last
                buycollect[i+1] = "{:.0f}".format(sum/sum_number)
                buycollect[i+2] = str(sum_number)
            else:
                pass
        #내용 모두 날리고 변경된 내용으로 새로 저장
        buypath= "/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/BUY.txt"
        file = open(buypath, 'w')
        for i in range(0,len(buycollect)):
            file.write(buycollect[i])
            file.write("\n")
        print("알림 : <매수를 완료했습니다.>")
        file.close()
        
    except:
        print("알림 : <매수 정보 수정 중 오류가 발생했습니다.>")

#매수 정보 여는 함수
def buy_open():
    try:
        buypath= "/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/BUY.txt"
        file = open(buypath, 'r')
        buycollect=file.read().splitlines()
        file.close()
        return buycollect
    except:
        print("알림 : <매수 정보 불러오는 중 오류가 발생했습니다.>")

#매도 정보 저장 함수
def sell_save(item, sellprice, sellnumber):
    try:
        sellreturn = item+"\n"+sellprice+"\n"+sellnumber
        sellpath= "/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/SELL.txt"
        file = open(sellpath, 'a')
        file.write(sellreturn.strip())
        file.write("\n")
        print("알림 : <매도를 완료했습니다.>")
    except:
        print("알림 : <매도 정보 저장 중 오류가 발생했습니다.>")
        
#매도 정보 여는 함수  
def sell_open():
    try:
        sellpath= "/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/SELL.txt"
        file = open(sellpath, 'r')
        sellcollect=file.read().splitlines()
        file.close()
        return sellcollect
    except:
        print("알림 : <매도 정보 불러오는 중 오류가 발생했습니다.>")

#손익 계산하여 저장하는 함수
def profit_and_loss(item, saveprice, sellprice, remainprice, remainnumber):
    try:
        get_saveprice = format(int(saveprice),',')
        buy = "매수 가격 : " + get_saveprice + "원"
        get_sellprice = format(int(sellprice),',')
        sell = "매도 가격 : " + get_sellprice + "원"

        profit = (int(sellprice) - int(saveprice)) / int(saveprice) *100
        profits = "수익률 : "+"{:0,.2f}".format(profit,',')+"%"

        realprofit = int(remainprice) * int(remainnumber)
        get_realprofit = format(realprofit,',')
        realprofits = "실현 손익 : " + get_realprofit + "원"

        get_remainnumber = format(int(remainnumber),',')
        sellnumber = "매도 수량 : " + get_remainnumber + "주"

        PLreturn = item+"\n"+buy+"\n"+sell+"\n"+sellnumber+"\n"+profits+"\n"+realprofits
        PLpath= "/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/PROFIT.txt"
        file = open(PLpath, 'a')
        file.write("========================================================\n")
        file.write(PLreturn.strip())
        file.write("\n")
        file.close()
    except:
        print("알림 : <손익 계산 중 오류가 발생했습니다.>")

#손익 정보 불러오는 함수
def pl_open():
    try:
        PLpath= "/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/PROFIT.txt"
        file = open(PLpath, 'r')
        PLcollect = file.read().splitlines()
        file.close()
        return PLcollect
    except:
        print("알림 : <손익 정보 불러오는 중 오류가 발생했습니다.>")

#종목과 매도수량 저장하는 함수
def stock_item_save(item, sellnumber):
    try:
        stockpath = "/FINANCE/LIST_PROJECT/LIST_CODE/STOCK_ITEM/"+item+".txt"
        file = open(stockpath, 'a')
        file.write(sellnumber.strip())
        file.write("\n")
        file.close()
    except:
        print("알림 : <매도량 저장 중 오류가 발생했습니다.>")

#매도량 오류 확인하는 함수
def stock_item_check(item, buynumber):
    try:
        stocknumber = 0
        stockpath = "/FINANCE/LIST_PROJECT/LIST_CODE/STOCK_ITEM/"+item+".txt"
        file = open(stockpath, 'r')
        stockcollect = file.read().splitlines()
        file.close()
        #총 매도량을 변수에 저장
        for i in range(0,len(stockcollect)):
            stocknumber += int(stockcollect[i])
        #총 매수량과 매도량의 크기를 비교함
        if(stocknumber > int(buynumber)):
            print("알림 : <매도량이 매수량을 초과하였습니다.>")
            checkcode = 0
        else:
            checkcode = 1
            pass
        return checkcode
    except:
        print("알림 : <매도량 확인 중 오류가 발생했습니다.>")

#매도량이 매수량을 넘은 경우 수정하는 함수
def stock_item_correct(item):
    try:
        stockpath = "/FINANCE/LIST_PROJECT/LIST_CODE/STOCK_ITEM/"+item+".txt"
        file = open(stockpath, 'r')
        stockcollect = file.read().splitlines()
        file = open(stockpath, 'w')
        #매도량이 매수량을 넘은 마지막 매도 수량을 제외하고 새롭게 저장 
        for i in range(0,len(stockcollect)-1):
            file.write(stockcollect[i])
            file.write("\n")
        file.close()
    except:
        print("알림 : <매도량 수정 중 오류가 발생했습니다.>")

#매도량 불러오는 함수
def stock_item_open(item):
    try:
        stocknumber = 0
        stockpath = "/FINANCE/LIST_PROJECT/LIST_CODE/STOCK_ITEM/"+item+".txt"
        file = open(stockpath, 'r')
        stockcollect = file.read().splitlines()
        file.close()
        for i in range(0,len(stockcollect)):
            stocknumber += int(stockcollect[i])    
        return stocknumber
    except:
        print("알림 : <매도량 불러오는 중 오류가 발생했습니다.>")

#포트폴리오 초기화
def portfolio_initialize(stock_item):
    try:
        item=[]
        Size = len(stock_item) / 3
        for i in range(0,int(Size)):
            #초기화할 종목을 리스트에 저장
            item.append(stock_item[3*i])   
            
        path="/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/BUY.txt"
        file = open(path, 'w')
        path="/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/PROFIT.txt"
        file = open(path, 'w')
        path="/FINANCE/LIST_PROJECT/LIST_CODE/PORTFOLIO/SELL.txt"
        file = open(path, 'w')   
        
        for j in range(0,len(item)):
            itempath = "/FINANCE/LIST_PROJECT/LIST_CODE/STOCK_ITEM/"+item[j]+".txt"
            itemfile = open(itempath, 'w')
            itemfile.close()
        file.close() 
    except:
        print("알림 : <포트폴리오 초기화 중 오류가 발생했습니다.>")