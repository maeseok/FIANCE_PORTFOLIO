#주식 포트폴리오

from bs4 import BeautifulSoup
import urllib.request as req
import pickle
import datetime
import requests

#매도 수익 계산 중 오류가 발생하면 그 값을 빼야함 SELL.txt에서
#완료 후 차트로 넘어감


#수익률 함수
def rate_import(code, firstdate, lastdate,item,nowDATE):
    #봇이 아님을 증명하는 값
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'}

    try:
        firstrate="0"
        lastrate="0"
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
                else :
                    pass
            #종료날 시세 불러오는 코드
            for i in range(1,len(date)+1):
                if(lastrate == "0"):
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
                if(firstrate == "0"):
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
            if (firstrate!="0" and lastrate!="0"):
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
        

#날짜 형식 수정 함수
def date_format(date):
    try:
        date = str(date).replace('-','.')
        return date
    except:
        print("알림 : <날짜 형식 수정 중 오류가 발생했습니다.")
        
#현재 시간 불러오는 함수
def time_format():
    try:
        now = datetime.datetime.now()
        nowDATE=now.strftime('%Y.%m.%d')
        return nowDATE
    except:
        print("알림 : <현재 시간을 불러오는 중 오류가 발생했습니다.")
#코드 DB연결 함수 
def db_connect():
    try:
        #DB(코드 값) 불러오기
        f = open('/FINANCE/LIST_PROJECT/DBandDB_SOURCE/COSPI.txt', 'rb')    
        f2 = open('/FINANCE/LIST_PROJECT/DBandDB_SOURCE/KOSDAQ.txt', 'rb')
        COSPI = pickle.load(f)
        KOSDAQ = pickle.load(f2)
        #종목 코드 값을 가진 딕셔너리 반환
        return COSPI,KOSDAQ
    except:
        print("알림 : <코드를 불러오는 중 오류가 발생했습니다.")
    finally:
        f.close()
        f2.close()
#종목 저장 함수
def finance_save(nowDATE):
    try:
        #해당 날짜 파일에 저장
        path="/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/FINANCE_DB/"+nowDATE+".txt"
        file = open(path, 'a')
        file.write(rate.strip())
        file.write("\n")
        print("알림 : <"+nowDATE+".txt 파일에 저장을 완료했습니다.>")

    except:
        print("알림 : <오류가 발생했습니다.>")

    finally:
        file.close()

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

#종목 입력을 통한 코드 생성 함수
def code_made(COSPI,KOSDAQ):
    item = input("종목 이름 입력 : ").replace(" ","")
    #코드 값 저장
    try:
        if(item in COSPI):
            code=COSPI[item]
                
        elif(item in KOSDAQ):
            code=KOSDAQ[item]
            
        return item,code
        item="\0"
    
    except:
        print("알림 : <코드 탐색 중 오류가 발생했습니다.>")

#입력 없이 코드만 생성하는 함수
def only_code_made(COSPI,KOSDAQ,item):
    #코드 값 저장
    try:
        if(item in COSPI):
            code=COSPI[item]
                
        elif(item in KOSDAQ):
            code=KOSDAQ[item]
            
        return code
    
    except:
        print("알림 : <코드 탐색 중 오류가 발생했습니다.>")

#수익률 출력하는 함수
def open_profit():
    try:
        itempath="/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/"+acitem+".txt"
        file = open(itempath, 'r')
        content = file.read().splitlines()
        file.close()
        return content
    except:
        print("알림 : <오류가 발생했습니다.>")
        
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
#수익률 초기화
def reset_profit(openitem):
    try:
        for i in range(0,len(openitem)):
            path = "/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/PROFIT_DB/"+openitem[i]+".txt"
            openfile = open(path, 'w')
    except:
        print("알림 : <수익률 초기화 중 오류가 발생했습니다.")
    finally:
        openfile.close()


        
#기본 setting
COSPI,KOSDAQ= db_connect()
nowDATE=time_format()
collect=[]


while True:
    
    print("\n=========================메뉴===========================")
    choice = input("1 : 포트폴리오 2 : 시세 조회 3 : 시세 출력 4 : 초기화 5 : 종료\n번호 : ")
    print("========================================================")
    

    #포트폴리오
    if (choice == "1"):
        print("=========================메뉴===========================")
        choice2 = input("1 : 매수  2 : 매도  3 : 포트폴리오 조회 4: 매도수익 \n번호 : ")
        print("========================================================")
        
        if(choice2 == "1"):
            try:
                #매수한 값을 가져옴
                get_buycollect = buy_open()
                item,code = code_made(COSPI,KOSDAQ)
                print("EX) 74900 7")
                buyprice = input("매수 가격 입력 : ")
                buynumber = input("매수량 입력(주) : ")

                print("=========================메뉴===========================")
                choice3 = input("1 : 종목 매수  2 : 나가기\n번호 : ")
                print("========================================================")
                if(choice3 == "1"):
                    #이미 매수한 종목인지 확인
                    if(item in get_buycollect):
                        #매수한 경우 원래 값 수정
                        buy_correct(item, buyprice, buynumber, get_buycollect)

                    else:
                        #새로 저장
                        buy_save(item, buyprice, buynumber)
                        continue

                elif(choice3 == "2"):
                    print("알림 : <메뉴로 돌아갑니다.>")
                    continue

                else:
                    print("알림 : <입력을 확인해주세요>")
                    continue
            except:
                print("알림 : <종목 매수 중 오류가 발생했습니다.>")
                
        elif(choice2 == "2"):
            try:
                item2,code2 = code_made(COSPI,KOSDAQ)
                print("EX) 75200 5")
                sellprice = input("매도 가격 입력 : ")
                sellnumber = input("매도량 입력(주) : ")

                print("=========================메뉴===========================")
                choice9 = input("1 : 종목 매도  2 : 나가기\n번호 : ")
                print("========================================================")
                if(choice9 == "1"):
                    #매수한 내용 불러옴
                    buycollect = buy_open()
                    for i in range(0,len(buycollect)):
                        if(buycollect[i] == item2):
                            saveprice = buycollect[i+1]
                            savenumber = buycollect[i+2]
                            remainprice = int(sellprice) - int(saveprice)
                            #매도량과 종목이름 저장
                            stock_item_save(item2, sellnumber)
                            #매도량이 매수량보다 많은지 확인
                            checkcode = stock_item_check(item2, savenumber)
                        else:
                            pass
                    #정상
                    if(checkcode == 1):
                        #매도한 정보 저장
                        sell_save(item2, sellprice, sellnumber)
                        #수익률 정보 저장
                        profit_and_loss(item2, saveprice, sellprice, remainprice, sellnumber)

                    #매도량이 매수량을 넘음
                    else:
                        #추가되어서 넘친 매도량 삭제
                        stock_item_correct(item2)
                        print("알림 : <매도 수량을 다시입력해주세요>")
                        continue

                elif(choice9 == "2"):
                    print("알림 : <메뉴로 돌아갑니다.>")
                    continue

                else:
                    print("알림 : <입력을 확인해주세요>")
                    continue
            except:
                print("알림 : <종목 매도 중 오류가 발생했습니다.>")
                
        #포트폴리오
        elif(choice2 == "3"):
            #포트폴리오 조회를 위한 리스트들
            try:
                Buyitem= []
                get_code = []
                get_profit = []
                get_presentrate = []
                get_presentprofit = []
                Buyremain=[]
                ptotal=[]
                ltotal=[]
                last_total=0
                present_total=0
                longline = "========================================================"

                #매수 정보 불러옴
                Buyinfor = buy_open()
                Sellinfor = sell_open()
                Size = len(Buyinfor) / 3
                for i in range(0,int(Size)):
                    #매수 종목을 리스트에 저장
                    Buyitem.append(Buyinfor[3*i])
                
                for i in range(0,len(Buyitem)):
                    for j in range(0,len(Buyinfor)):
                        if(Buyitem[i] == Buyinfor[j]): #종목 이름이 들어있는 항목의 위치를 찾음
                            #매도한 내용이 있는지 확인
                            if(len(Sellinfor) != 0):
                                for p in range(0,len(Sellinfor)):
                                    if(Buyinfor[j] == Sellinfor[p]):
                                        #해당 종목의 매도량을 저장함
                                        stocknumber = stock_item_open(Buyitem[i])
                                        #현재 남은 수량을 저장함
                                        Buyremain = int(Buyinfor[j+2]) - stocknumber
                                        #리스트에 최신화(리스트를 이용하여 출력할 것이기 때문이다.)
                                        Buyinfor[j+2] = Buyremain 
                                        #코드만 불러옴 
                                    else:
                                        Buyremain = Buyinfor[j+2]
                            
                            else:
                                #매도 내용이 없으면 현재 수량을 남은 수량으로 저장
                                Buyremain = Buyinfor[j+2]
                            #최종적으로 종목을 출력 형식에 맞게 값을 변형시킴
                            get_code = only_code_made(COSPI,KOSDAQ,Buyitem[i])   
                            get_profit, get_presentrate, get_presentprofit,get_ptotal,get_ltotal = present_rate(get_code,Buyitem[i],Buyinfor[j+1],Buyremain) 
                            ptotal.append(get_ptotal)
                            ltotal.append(get_ltotal)
                            Buyinfor.insert(j+2,get_presentrate)
                            Buyinfor.insert(j+3,get_profit)
                            Buyinfor.insert(j+5,get_presentprofit)
                            Buyinfor.insert(j+6,longline)
                        else:
                            pass

                for l in range(0, len(Buyinfor)):
                    if(Buyinfor[l] == 0):
                        #만약 남은 수량이 0이라면 해당 정보가 출력되지 않게 삭제함
                        del Buyinfor[l-4:l+3]
                        break
                    else:
                        pass

                #입력된 내용을 형식적으로 다듬는 과정
                for k in range(0,len(Buyinfor)):
                    if(k%7 == 1 ):
                        average_rate = Buyinfor[k]
                        get_average = format(int(average_rate),',')
                        average = "평단가 : "+ get_average+"원"
                        Buyinfor[k] = average
                    elif(k%7 == 4):
                        amount = Buyinfor[k]
                        get_amount = format(int(amount),',')
                        stock_amount = "수량 : " + get_amount+"주"
                        Buyinfor[k] = stock_amount
                    else:
                        pass

                #최종 내용 출력
                for u in range(0,len(Buyinfor)):
                    print(Buyinfor[u])
                    
                for n in range(0,len(ltotal)):
                    last_total += ltotal[n] 
                    present_total += ptotal[n] 
                #형식에 맞게 값 저장
                get_latotal = format(last_total,',')
                get_prtotal = format(present_total,',')
                if(present_total-last_total== 0):
                    print("구매 총합 : "+get_latotal+"원")
                    print("현재 총합 : "+get_prtotal+"원")
                else:
                    total_profit = (present_total-last_total)/last_total*100
                    print("구매 총합 : "+get_latotal+"원")
                    print("현재 총합 : "+get_prtotal+"원")
                    print("총 수익률 : "+"{:0,.2f}".format(total_profit)+"%")
            except:
                print("알림 : <포트폴리오 조회 중 오류가 발생했습니다.>")
                
            
        elif(choice2 == "4"):
            #매도한 수익 정보가 저장된 함수 불러옴
            try:
                PLcollect = pl_open()
                print("매도 수익")
                for i in range(0,len(PLcollect)):
                    print(PLcollect[i])
            except:
                print("알림 : <매도 수익 조회 중 오류가 발생했습니다.>")

        else:
            print("알림 : <오류가 발생했습니다.>")
    #조회      
    elif(choice == "2"):
        print("=========================메뉴===========================")
        choice4= input("1 : 오늘의 시세 2 : 수익률 조회\n번호 : ")
        print("========================================================")
        
        if(choice4 == "1"):
            try:
                #코드 생성하는 함수 불러옴
                item3,code3 = code_made(COSPI,KOSDAQ)

                #입력 종목 페이지 저장
                url="https://finance.naver.com/item/main.nhn?code="+code3
                #페이지 코드 변수에 저장
                res=req.urlopen(url)
                soup = BeautifulSoup(res,"html.parser")
                #변수에서 종목 내용 찾고 텍스트만 변수에 저장 후 출력 
                rate2=soup.select_one("div.rate_info>dl.blind")
                rate=nowDATE+rate2.get_text()
                print("========================================================")
                print(rate)
                print("=========================메뉴===========================")
                choice5= input("1 : 저장 2 : 나가기\n번호 : ")
                print("========================================================")
                if(choice5 == "1"):
                    finance_save(nowDATE)
                    continue
                elif(choice5 == "2"):
                    continue
                else:
                    print("알림 : <입력을 확인해주세요>")
                    continue
            except:
                print("알림 : <오류가 발생했습니다. 메뉴로 돌아갑니다.>")
                continue                

        elif(choice4 == "2"):
            try:
                #코드 만드는 함수 불러옴
                item4,code4 = code_made(COSPI,KOSDAQ)

                fdate2=input("매수 날짜 입력 : ")
                firstdate2=date_format(fdate2)

                ldate=input("매도 날짜 입력 : ")
                lastdate2=date_format(ldate)
                #날짜 오류 검증
                checkfirst = firstdate2.replace(".","")
                checklast = lastdate2.replace(".","")

                if(int(checkfirst)>int(checklast)):
                    print("알림 : <날짜를 다시 입력해주세요.>")
                    continue

                else:
                    #수익률 정보 불러옴
                    print("=========================결과===========================")
                    profit,first,last = rate_import(code4,firstdate2,lastdate2,item4,nowDATE)
                    print("=========================메뉴===========================")
                    
                    choice6= input("1 : 저장 2 : 나가기\n번호 : ")
                    print("========================================================")

                    if(choice6 == "1"):
                        profit_save(item4,first,last,profit)
                        save_item(item4)

                    elif(choice6 == "2"):
                        print("알림 : <메뉴로 돌아갑니다.>")
                        continue

                    else:
                        print("알림 : <입력을 확인해주세요>")
                        continue
            except:
                print("알림 : <오류가 발생했습니다. 메뉴로 돌아갑니다.>")
                continue                          

    #출력
    elif(choice == "3"):
        print("=========================메뉴===========================")
        choice7 = input("1 : 종목 정보 출력  2 : 수익률 정보 출력 3 : 나가기\n번호 : ")
        
        if(choice7 == "1"):
            try:
                print("EX)"+nowDATE)
                acdate = input("접속할 날짜 입력 : ")
                #입력한 날짜 형식을 일정한 형태로 수정하는 함수 불러옴
                date=date_format(acdate)
                datepath="/FINANCE/LIST_PROJECT/LIST_CODE/INQUIRY/FINANCE_DB/"+date+".txt"
                file = open(datepath, 'r')
                collect = file.read().splitlines()
                name = input("종목 이름 입력 : ")
                if(name in collect):
                    #리스트 내포를 이용하여 특정 종목이 있는 위치를 알아내서 x에 저장함
                    i = [i for i, s in enumerate(collect) if s == name]
                    for x in i:
                        pass
                    print("========================================================") 
                    #종목의 시작과 끝의 길이를 지정하여 출력함
                    for x in range(x-1,x+4):
                        print(collect[x])
                else:
                    print("알림 : <확인 후 다시 입력하세요.>")
                    continue
            except:
                print("알림 : <종목 정보 출력 중 오류가 발생했습니다.")


        #수익률 출력
        elif(choice7 == "2"):
            try:
                print("=========================메뉴===========================")
                choice8 = input("1 : 전체 출력  2 : 날짜 출력 3 : 나가기\n번호 : ")

                if(choice8 == "1"):
                    print("EX) 삼성전자")
                    acitem = input("접속할 종목 입력 : ")
                    #특정 종목의 저장한 수익률 정보를 가져옴
                    content = open_profit()
                    print("========================="+acitem+"===========================")
                    for i in range(0,len(content),5):
                        x=i
                    for j in range(0, len(content)):
                        #종목 이름은 나오지 않게 설정
                        if(content[j]!=content[x]):
                            print(content[j])
                        else:
                            pass

                elif(choice8 == "2"):
                    print("EX) 삼성전자")
                    acitem = input("접속할 종목 입력 : ")
                    content = open_profit()
                    bdate = input("매수한 날짜 입력 : ")
                    buydate = date_format(bdate)
                    sdate = input("매도한 날짜 입력 : ")
                    selldate = date_format(sdate)
                    checkbuy = buydate.replace(".","")
                    checksell = selldate.replace(".","")
                    print("========================================================")

                    if(int(checkbuy)>int(checksell)):
                        print("알림 : <날짜를 다시 입력해주세요.>")
                        continue
                    else:
                        for i in range(0,len(content)):
                            if (buydate in content[i] ):
                                x=i
                                if("매수" in content[x]):
                                    if(selldate in content[x+1]):
                                        for x in range(x-1,x+3):
                                            print(content[x])
                                    else : 
                                        pass
                                else :
                                    pass             
                            else:
                                pass
                elif(choice8 == "3"):
                    print("알림 : <메뉴로 돌아갑니다.>")

                else :
                    print("알림 : <확인 후 다시 입력하세요.>")
                    continue
            except:
                print("알림 : <수익률 출력 중 오류가 발생했습니다.>")

        #나가기
        elif(choice7 == "3"):
            print("알림 : <메뉴로 돌아갑니다.>")
            continue            

        else:
            print("알림 : <오류가 발생했습니다.>")
            continue   
    #초기화
    elif(choice =="4"):
        print("=========================메뉴===========================")
        choice9 = input("1 : 포트폴리오 초기화  2 : 수익률 조회 초기화 3 : 나가기\n번호 : ")
        #포트폴리오 초기화
        if(choice9 == "1"):
            try:
                print("알림 : <정말로 포트폴리오를 초기화 하시겠습니까?>")
                get_choice="\0"
                get_choice = input("Y or N : ")
                if(get_choice == "Y"):
                    stock_item = buy_open()
                    portfolio_initialize(stock_item)
                    print("알림 : <초기화를 완료하였습니다.>")
                elif(get_choice == "N"):
                    print("알림 : <메뉴로 돌아갑니다.>")
                    continue
                else:
                    print("알림 : <입력을 확인해주세요>")
                    continue
            except:
                print("알림 : <초기화 중 오류가 발생했습니다.>")
        #수익률 조회 초기화
        elif(choice9 == "2"):
            openitem = open_item() 
            get_choice="\0"
            get_choice = input("Y or N : ")
            if(get_choice == "Y"):
                reset_item()
                reset_profit(openitem)
                print("알림 : <초기화를 완료하였습니다.>")
            elif(get_choice == "N"):
                print("알림 : <메뉴로 돌아갑니다.>")
                continue
            else:
                print("알림 : <입력을 확인해주세요>")
                continue

        #나가기
        elif(choice9 == "3"):
            print("알림 : <메뉴로 돌아갑니다.>")
            continue
        else:
            print("알림 : <입력을 확인해주세요.>")
            continue
        
    #종료
    elif(choice == "5"):
        print("알림 : <프로그램을 종료합니다.>")
        break 

        
    else:
        print("알림 : <잘못 입력했습니다. 다시 입력하세요>")


