import os
import cv2
import numpy as np
import tensorflow as tf

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

red_color = (0, 0, 255)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# 모델 불러오기
load_model = tf.keras.models.load_model('acc_07099.h5')

while True:
    ret, cam = cap.read()

    if ret:
        cam = cv2.rectangle(cam, (200, 120), (440, 380), red_color, 3)
        cv2.imshow('camera', cam)
        dst = cam.copy()
        roi = cam[123:377, 203:437]
        dst = cv2.resize(roi, dsize=(224, 224), interpolation=cv2.INTER_AREA)
        '''
        #이미지 저장
        img_save= cv2.imwrite('test.jpg', dst)
        '''

        # predict
        b = np.expand_dims(dst, axis=0)
        predict = load_model.predict(x=b)

        label = np.argmax(predict)
        #0:blouse 1:hoodie 2:shirt
        print(np.argmax(predict))

        if label==0:
            choice= "Blouse"
        elif label==1:
            choice="Hoodie"
        else:
            choice="T-shirt"

        #cv2.putText(dst,choice,(10,60), cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0), 2,cv2.LINE_AA)
        cv2.imshow("dst", dst)
        if cv2.waitKey(1) & 0xFF == 27:
            break  # esc 키 누르면 닫힘

cap.release()
cv2.destroyAllWindows()

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import pandas as pd
import serial

ard = serial.Serial(
    #포트는 실행 전에 확인
    port = 'COM8',
    baudrate = 9600
    )

#DataFrame 생성
data_v1=[[0,0,0],
         [0,0,0],
         [0,0,0],
         [0,0,0]]

index_v1=['S','M','L','XL']

columns_v1=['Blouse_A','Hoodie_A','T-shirt_A']

v1=pd.DataFrame(data=data_v1, index=index_v1, columns=columns_v1)


j=0
i=0

def check_inventory(v1):
    for k in range(5):
        listen = ard.readline()
        x = listen.decode('utf-8')[:-2]
        if x != '':
            # print(float(x))
            distance = float(x)
            if (distance > 20 and distance <= 30):
                # 재고=1
                v1.iloc[j][i] = 1
            elif (distance > 10 and distance <= 20):
                # 재고=2
                v1.iloc[j, i] = 2
            elif (distance > 0 and distance <= 10):
                # 재고=3
                v1.iloc[j][i] = 3
            else:
                # shirt=0
                v1.iloc[j][i] = 0

        # print(v1)
    return v1

print("****************결과**************\n",check_inventory(v1))
#v1= check_inventory(v1)

class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Stock_Check')
        self.resize(500, 500)

        self.line_edit = QLineEdit(self)
        self.line_edit.move(150, 280)
        self.line_edit.resize(200,40)

        global label

        if label==0:
            choice="Blouse"
        elif label==1:
            choice="Hoodie"
        else:
            choice="T-shirt"


        self.text_label = QLabel(self)
        self.text_label.move(60, 220)
        self.text_label.setText(f'You chose {choice}! Check it out!!')
        self.text_label.setFont(QtGui.QFont("궁서",15))
        self.text_label.setStyleSheet("Color: green")
        self.text_label.adjustSize()

        self.button = QPushButton(self)
        self.button.move(100,350)
        self.button.setText('Stock')
        self.button.clicked.connect(self.button_event)

        self.addbutton = QPushButton(self)
        self.addbutton.move(200, 350)
        self.addbutton.setText('Order')
        self.addbutton.clicked.connect(self.orderbutton_event)

        self.deletebutton = QPushButton(self)
        self.deletebutton.move(300, 350)
        self.deletebutton.setText('Delete')
        self.deletebutton.clicked.connect(self.deletebutton_event)

        self.msg = QMessageBox()


        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)

        global v1



        for i in range(len(v1.index)):
            for j in range(len(v1.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(v1.iloc[i, j])))
        self.tableWidget.setHorizontalHeaderLabels(["Blouse A", "Hoodie A","T-shirt A"])
        self.tableWidget.setVerticalHeaderLabels(["S","M","L","XL"])

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addStretch(3)
        self.setLayout(layout)

        self.show()


        self.show()


    def button_event(self):
        global v1

        text = self.line_edit.text()  # line_edit text 값 가져오기
        if text =='A,S':
            stock = v1.iloc[0][0]
            self.text_label.setText("   "+str(stock)+" Left")  # label에 text 설정하기

        elif text=='A,M':
            stock = v1.iloc[1][0]
            self.text_label.setText("   "+str(stock)+" Left")  # label에 text 설정하기
        else:
            stock = v1.iloc[2][0]
            self.text_label.setText("   "+str(stock)+" Left")  # label에 text 설정하기

    def deletebutton_event(self):
        text = self.line_edit.text()  # line_edit text 값 가져오기
        if text=='A,S':
            self.text_label.setText(text+' Delete')  # label에 text 설정하기
            c = 'y'
            c = c.encode('utf-8')
            ard.write(c)

    def orderbutton_event(self):
        text = self.line_edit.text()
        if text == 'A,S':
            self.text_label.setText(text+' Order')  # label에 text 설정하기
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle('Blouse A S-size')
            self.msg.setText('Order Complete')
            self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = self.msg.exec_()

            # 반환값 판단
            print('QMessageBox 리턴값 ', retval)
            if retval == QMessageBox.Ok:
                print('messagebox ok : ', retval)
            elif retval == QMessageBox.Cancel:
                print('messagebox cancel : ', retval)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()

    sys.exit(app.exec_())
