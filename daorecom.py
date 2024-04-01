import cx_Oracle

def changeName(rmtype):
    if rmtype == 1: rmtype = "STD"
    elif rmtype == 2: rmtype = "STT"
    elif rmtype == 3: rmtype = "STF"
    elif rmtype == 4: rmtype = "DRD"
    elif rmtype == 5: rmtype = "DRT"
    elif rmtype == 6: rmtype = "DRF"
    elif rmtype == 7: rmtype = "SUD"
    elif rmtype == 8: rmtype = "SUT"
    elif rmtype == 9: rmtype = "SUF"
    elif rmtype == 10: rmtype = "SPA"
    elif rmtype == 11: rmtype = "OND"
    elif rmtype == 12: rmtype = "PTY"
    else: rmtype = "X"
    return rmtype

class DaoRecom:
    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
        
    def selectRecom(self):
        sql = """
            SELECT 
                RERM_AGE
                , RERM_NMPR
                , RERM_CHILD_YN
                , RERM_RMTYPE
            FROM    
                TB_RECOM_RM;
        """
        self.cur.execute(sql)
        recom = self.cur.fetchall()
        myjson = []
        for r in recom:
            myjson.append({'age':r[0], 'nmpr':r[1], 'child_yn':r[2], 'rmtype':r[3]})
        return myjson
    
    def insertRecom(self, age, nmpr, rmtype, rank):
        chrmtype = changeName(rmtype)
        sql = f"""
            INSERT INTO TB_RECOM_RM(
                RERM_AGE
                , RERM_NMPR
                , RERM_RMTYPE
                , RERM_RANK
            )VALUES(
                '{age}'
                , '{nmpr}'
                , '{chrmtype}'
                , '{rank}'
            )
        """
        self.cur.execute(sql)
        self.conn.commit()
        
        rowcnt = self.cur.rowcount
        
        return rowcnt
    
    def insertrecomRm(self):
        sql = f"""
        INSERT INTO 
            TB_RECOM_RM (
                RERM_AGE
                , RERM_NMPR
                , RERM_RMTYPE
                , RERM_RANK
            )
            SELECT 
                RERM_AGE
                , RERM_NMPR
                , RERM_RMTYPE
                , rank
            FROM (
                SELECT 
                    RERM_AGE
                    , RERM_NMPR
                    , RERM_RMTYPE
                    , room_count
                    , ROW_NUMBER() OVER(PARTITION BY RERM_AGE, RERM_NMPR ORDER BY room_count DESC) AS rank
                FROM (
                    SELECT 
                        RERM_AGE
                        , RERM_NMPR
                        , RERM_RMTYPE
                        , COUNT(*) AS room_count
                    FROM 
                        TB_RECOM_RM_USE
                    GROUP 
                        BY RERM_AGE, RERM_NMPR, RERM_RMTYPE
                )
            ) WHERE 
                rank <= 2
            ORDER BY 
                RERM_AGE, RERM_NMPR, room_count DESC
        """
        self.cur.execute(sql)
        self.conn.commit()
        
        rowcnt = self.cur.rowcount
        
        return rowcnt
    
    def __del__(self):
        self.cur.close()
        self.conn.close()
        
if __name__ == "__init__":
    dr = DaoRecom()
    
if __name__ == "__main__":
    dr = DaoRecom()
    print(dr.selectRecom())