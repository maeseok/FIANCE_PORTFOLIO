#주식 포트폴리오
from bs4 import BeautifulSoup
import urllib.request as req
import pickle
import datetime
import requests
#def code import
import inquiry
import portfolio
import basic

#기본 setting
COSPI,KOSDAQ= basic.db_connect()
nowDATE=basic.time_format()
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
                get_buycollect = portfolio.buy_open()
                item,code = basic.code_made(COSPI,KOSDAQ)
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
                        portfolio.buy_correct(item, buyprice, buynumber, get_buycollect)

                    else:
                        #새로 저장
                        portfolio.buy_save(item, buyprice, buynumber)
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
                item2,code2 = basic.code_made(COSPI,KOSDAQ)
                print("EX) 75200 5")
                sellprice = input("매도 가격 입력 : ")
                sellnumber = input("매도량 입력(주) : ")

                print("=========================메뉴===========================")
                choice9 = input("1 : 종목 매도  2 : 나가기\n번호 : ")
                print("========================================================")
                if(choice9 == "1"):
                    #매수한 내용 불러옴
                    buycollect = portfolio.buy_open()
                    for i in range(0,len(buycollect)):
                        if(buycollect[i] == item2):
                            saveprice = buycollect[i+1]
                            savenumber = buycollect[i+2]
                            remainprice = int(sellprice) - int(saveprice)
                            #매도량과 종목이름 저장
                            portfolio.stock_item_save(item2, sellnumber)
                            #매도량이 매수량보다 많은지 확인
                            checkcode = portfolio.stock_item_check(item2, savenumber)
                        else:
                            pass
                    #정상
                    if(checkcode == 1):
                        #매도한 정보 저장
                        portfolio.sell_save(item2, sellprice, sellnumber)
                        #수익률 정보 저장
                        portfolio.profit_and_loss(item2, saveprice, sellprice, remainprice, sellnumber)

                    #매도량이 매수량을 넘음
                    else:
                        #추가되어서 넘친 매도량 삭제
                        portfolio.stock_item_correct(item2)
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
                Buyinfor = portfolio.buy_open()
                Sellinfor = portfolio.sell_open()
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
                                        stocknumber = portfolio.stock_item_open(Buyitem[i])
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
                            get_code = basic.only_code_made(COSPI,KOSDAQ,Buyitem[i])   
                            get_profit, get_presentrate, get_presentprofit,get_ptotal,get_ltotal = portfolio.present_rate(get_code,Buyitem[i],Buyinfor[j+1],Buyremain) 
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
                PLcollect = portfolio.pl_open()
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
                item3,code3 = basic.code_made(COSPI,KOSDAQ)

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
                    inquiry.finance_save(nowDATE,rate)
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
                item4,code4 = basic.code_made(COSPI,KOSDAQ)

                fdate2=input("매수 날짜 입력 : ")
                firstdate2=basic.date_format(fdate2)

                ldate=input("매도 날짜 입력 : ")
                lastdate2=basic.date_format(ldate)
                #날짜 오류 검증
                checkfirst = firstdate2.replace(".","")
                checklast = lastdate2.replace(".","")

                if(int(checkfirst)>int(checklast)):
                    print("알림 : <날짜를 다시 입력해주세요.>")
                    continue

                else:
                    #수익률 정보 불러옴
                    print("=========================결과===========================")
                    profit,first,last = inquiry.rate_import(code4,firstdate2,lastdate2,item4,nowDATE)
                    print("=========================메뉴===========================")
                    
                    choice6= input("1 : 저장 2 : 나가기\n번호 : ")
                    print("========================================================")

                    if(choice6 == "1"):
                        inquiry.profit_save(item4,first,last,profit)
                        inquiry.save_item(item4)

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
        print("알림 : <시세 출력은 시세 조회를 통해 저장한 값을 가져오는 역할을 합니다.>")
        print("=========================메뉴===========================")
        choice7 = input("1 : 종목 정보 출력  2 : 수익률 정보 출력 3 : 나가기\n번호 : ")
        
        if(choice7 == "1"):
            try:
                print("EX)"+nowDATE)
                acdate = input("접속할 날짜 입력 : ")
                #입력한 날짜 형식을 일정한 형태로 수정하는 함수 불러옴
                date=basic.date_format(acdate)
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
            #try:
            print("=========================메뉴===========================")
            choice8 = input("1 : 전체 출력  2 : 날짜 출력 3 : 나가기\n번호 : ")

            if(choice8 == "1"):
                print("EX) 삼성전자")
                acitem = input("접속할 종목 입력 : ")
                #특정 종목의 저장한 수익률 정보를 가져옴
                content = inquiry.open_profit(acitem)
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
                content = inquiry.open_profit(acitem)
                bdate = input("매수한 날짜 입력 : ")
                buydate = basic.date_format(bdate)
                sdate = input("매도한 날짜 입력 : ")
                selldate = basic.date_format(sdate)
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
            #except:
                #print("알림 : <수익률 출력 중 오류가 발생했습니다.>")

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
                    stock_item = portfolio.buy_open()
                    portfolio.portfolio_initialize(stock_item)
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
            openitem = inquiry.open_item() 
            get_choice="\0"
            get_choice = input("Y or N : ")
            if(get_choice == "Y"):
                inquiry.reset_item()
                inquiry.reset_profit(openitem)
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


