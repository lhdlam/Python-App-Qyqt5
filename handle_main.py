from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_MainWindow

class Handle_Main(Ui_MainWindow):
  def __init__(self, mainwindow):
    # self.setupUi(MainWindow)
    self.setupUi(mainwindow)
    
    self.stackedWidget.setCurrentWidget(self.page_1)
    
    self.btn1.clicked.connect(lambda: self.changePage(1))
    self.btn2.clicked.connect(lambda: self.changePage(2))
    self.btn3.clicked.connect(lambda: self.changePage(3))
    self.btn4.clicked.connect(lambda: self.changePage(4))
    
    self.btn1_4.clicked.connect(lambda: self.changePage(2))
    
    
  def changePage(self, index):
    if index ==1:
      self.stackedWidget.setCurrentWidget(self.page_1)
    elif index == 2:
      self.stackedWidget.setCurrentWidget(self.page_2)
    elif index == 3:  
      self.stackedWidget.setCurrentWidget(self.page_3)
    elif index == 4:  
      self.stackedWidget.setCurrentWidget(self.page_4)
        
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Handle_Main()
    MainWindow.show()
    sys.exit(app.exec_())