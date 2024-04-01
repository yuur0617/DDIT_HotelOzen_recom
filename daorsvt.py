import cx_Oracle
from datetime import datetime
import numpy as np

# ===========================
# 예약 다오
# ===========================

def convertBinaryS(number):
    binary_representation = bin(number)[2:]  
    filled_binary = binary_representation.zfill(6)
    return filled_binary

def convertBinaryF(number):
    binary_representation = bin(number)[2:]  
    filled_binary = binary_representation.zfill(4)
    return filled_binary

class DaoRsvt:
    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
        
    #예약 내역 조회 메서드
    def selectList(self):
        sql="""
            SELECT 
                CST_NO
                ,CHKIN_NO
                ,CI_TOTAL_NMPR
                ,RMT_TYPE_CD
                ,TO_CHAR(CST_BIRTH, 'YYYY/MM/DD') AS BIRTHDATE
            FROM TB_CHKIN 
                INNER JOIN 
                (SELECT     
                    RMT_TYPE_CD, RM_NO
                FROM TB_ROOM 
                    INNER JOIN TB_ROOM_TYPE USING(RMT_TYPE_CD)) USING(RM_NO)
                INNER JOIN TB_CSTMR USING(CST_NO)
        """    
        self.cur.execute(sql)
        
        chkin_list = self.cur.fetchall()
        
        myjson = []
        for m in chkin_list:
            cst_no = m[0]
            chkin_no = m[1]
            total_cnt = m[2]
            room_type = m[3]
            birthdate = datetime.strptime(m[4], '%Y/%m/%d')
            
            age = self.calculate_age(birthdate)
            
            myjson.append({'cst_no': cst_no, 'chkin_no': chkin_no, 'total_cnt': total_cnt
                           , 'room_type': room_type, 'age': age})
        return myjson
    
    #생년월일 데이터를 나이로 출력하는 메서드(10의자리만)
    def calculate_age(self, birthdate):
        today = datetime.now()
        age = today.year - birthdate.year
        age = int((age + 1)/10)
        return age
    
    def getXtYs(self):
        sql = f'''
            SELECT 
                CI_TOTAL_NMPR
                ,TO_CHAR(CST_BIRTH, 'YYYY/MM/DD') AS BIRTHDATE
                ,DECODE(RMT_TYPE_CD ,'STD','1'
                                        ,'STT','2'
                                        ,'STF','3'
                                        ,'DRD','4'
                                        ,'DRT','5'
                                        ,'DRF','6'
                                        ,'SUD','7'
                                        ,'SUT','8'
                                        ,'SUF','9'
                                        ,'SPA','10'
                                        ,'OND','11'
                                        ,'PTY','12') ROOM_TYPE
            FROM 
                TB_CHKIN 
                INNER JOIN 
                    (SELECT     
                        RMT_TYPE_CD, RM_NO
                    FROM TB_ROOM 
                        INNER JOIN TB_ROOM_TYPE USING(RMT_TYPE_CD)) USING(RM_NO)
                INNER JOIN TB_CSTMR USING(CST_NO)  
        '''
        self.cur.execute(sql)
        rsvt_list = self.cur.fetchall()
        
        xt = []
        yt = []
        for i in rsvt_list:
            birthdate = datetime.strptime(i[1], '%Y/%m/%d')
            age = self.calculate_age(birthdate)
            
            print(i[0])
            print(age)
            print(i[2])
            print("----------")
            
            xt.append(list(convertBinaryS(i[0]))+list(convertBinaryF(age)))
            yt.append(i[2])
        
        x_train = np.array(xt)
        x_train = x_train.astype(int)
        y_train = np.array(yt)
        
        return x_train, y_train
        
        def __del__(self):
            self.cur.close()
            self.conn.close()
        
if __name__ == '__main__':
    drs = DaoRsvt()
    # print(drs.selectList())
    print(drs.getXtYs())
