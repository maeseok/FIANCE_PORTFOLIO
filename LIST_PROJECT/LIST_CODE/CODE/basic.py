import datetime
import pickle


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