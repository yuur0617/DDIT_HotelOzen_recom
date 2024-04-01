import tensorflow as tf
import numpy as np
import cx_Oracle
from recom.daoroomtype import DaoRoomType
from recom.daorsvt import DaoRsvt
from recom.daorecom import DaoRecom

class AaoRecom:
    def __init__(self):
        self.drt = DaoRoomType()
        self.drs = DaoRsvt()
        self.dr = DaoRecom()
        
        self.cnt = self.drt.getCnt()
        
        self.x_train = None
        self.y_train = None
        
        self.label_name = self.drs.selectList()
        
        self.setXYTrain()
    
    def setXYTrain(self):
        self.x_train, self.y_train = self.drs.getXtYs()
        
    #신경망 메서드
    def pred(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(10,)),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dense(1024, activation=tf.nn.relu),
            tf.keras.layers.Dense(self.cnt, activation=tf.nn.softmax)
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        self.y_train = self.y_train.astype(int)
       
        model.fit(self.x_train, self.y_train, epochs=20)
        pred = model.predict(self.x_train)
        model.summary()
        
        for idx,i in enumerate(pred):
            try:
                myidx = np.argmax(i)
                print(self.label_name[idx]['age'], self.label_name[idx]['total_cnt'], myidx, 1)
                # self.dr.insertRecom(self.label_name[idx]['age'], self.label_name[idx]['total_cnt'], myidx, 1)
                
                i[myidx] = 0
                myidx2 = np.argmax(i)
                print(self.label_name[idx]['age'], self.label_name[idx]['total_cnt'], myidx, 2)
                # self.dr.insertRecom(self.label_name[idx]['age'], self.label_name[idx]['total_cnt'], myidx2, 2)
                
            except cx_Oracle.DatabaseError as e:
                print(e)
                continue
        
if __name__ == '__main__' :
    ar = AaoRecom()
    ar.pred()
        