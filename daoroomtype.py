import cx_Oracle

# ===========================
# 객실타입 다오
# ===========================

class DaoRoomType :
    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
    
    #객실 종류 갯수 넘버링 메서드
    def getCnt(self):
        sql = """
            SELECT 
                COUNT(*)
            FROM TB_ROOM_TYPE
        """
        self.cur.execute(sql)
        cnt = self.cur.fetchone()
        return cnt[0]+1
    
    # 객실타입 라벨링 메서드
    def getLabels(self):
        sql = """
            SELECT 
                RMT_LABEL, RMT_TYPE_CD
            FROM 
                TB_ROOM_TYPE
        """
        self.cur.execute(sql)
        room_type_list = self.cur.fetchall()
        myjson = []
        for m in room_type_list:
            myjson.append({'room_label':m[0], 'room_cd':m[1]})
        return myjson
    
    def __del__(self):
        self.cur.close()
        self.conn.close()
                
if __name__ == '__main__':
    drt = DaoRoomType()
    print(drt.getCnt())
    print(drt.getLabels())
