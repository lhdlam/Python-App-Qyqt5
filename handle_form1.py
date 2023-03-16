from form1 import Ui_Form1


class Handle_Form1(Ui_Form1):
  def __init__(self, mainwindow):
    self.setupUi(mainwindow)
    self.form1 = mainwindow
  def closeEvent(self, event):
      # Nhận sự kiện click close form1
      self.form1.reject()
      print("exit!!")