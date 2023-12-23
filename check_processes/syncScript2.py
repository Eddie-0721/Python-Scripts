import pymysql,datetime
import time

def conn():
    return pymysql.connect(host="10.18.101.44",port=3306,user="investor",password="investor", database="investor", charset="utf8")

def selectSync(brokerCode:str):
    selectSyncRecordSql="select tpb.SYNC_STATUS  ,tsr.LAST_SYNC_TIME  from t_product_bus tpb left join t_sync_record tsr on tpb.SC_NO =tsr.BROKER_CODE where tpb.sc_no='{brokerCode}';".format(brokerCode=brokerCode)
    connection=conn()
    cursor=connection.cursor()
    
    try:
        cursor.execute(selectSyncRecordSql)
    except:
        print("fetch err")
    finally:
        cursor.close()
        connection.close()
        
    syncRecord=cursor.fetchall()
    return syncRecord

def compareWithTime(brokerCode:str,setInterval=20):
    syncRecordList=selectSync(brokerCode)
    if(len(syncRecordList)==0):
        return True
    if(syncRecordList[0][0]==0):
        return True
    currTimePoint=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for syncRecord in syncRecordList:
        interval=datetime.datetime.strptime(currTimePoint,"%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(syncRecord[1],"%Y-%m-%d %H:%M:%S")
        if interval.total_seconds() > setInterval: return False
    return True

def traverseBrokerCode(brokerCodeList:list,setInterval=20):
    ExceptMap={}
    for brokerCode in brokerCodeList:
        ExceptMap[brokerCode]=compareWithTime(brokerCode,setInterval)
    return ExceptMap


if __name__=="__main__":
    start = start = time.time()
    print(traverseBrokerCode(["tfzq"]))
    end = time.time()
    print (end-start)