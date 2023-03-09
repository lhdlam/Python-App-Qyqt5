from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QTableWidgetItem
from PyQt5 import QtCore
from handle_form1 import Handle_Form1
from handle_main import Handle_Main

import openpyxl

class UI():
  def __init__(self):
    
    self.mainUI = QMainWindow()
    self.mainHandle = Handle_Main(self.mainUI)
    self.mainHandle.btn1_1.clicked.connect(lambda: self.selectFile())
    self.mainHandle.table_excel.cellChanged.connect(self.onCellChanged)
    self.mainHandle.btn1_4.clicked.connect(lambda: self.export_data_screen_1())
    self.row = 1
    self.column = 1
    
    
    self.mainUI.show()
     
     
     
  def loadMainForm(self, data):
    # self.mainUI.hide()
    self.form1 = QDialog()
    self.form1Handle = Handle_Form1(self.form1)
    self.form1Handle.setupUi(self.form1)
    self.form1Handle.btn_select_file.clicked.connect(lambda: self.selectFile())
    self.form1Handle.btn_submit.clicked.connect(lambda: self.show_data_excel())
    self.form1.exec()
    
        
  def selectFile(self):
    dir = "D:\\Scropper\\app_desktop\\data"
    filters = "Excel files (*.xlsx)"
    selected_filter = "Excel (*.xlsx)"
    # options = "" # ???
    fname = QFileDialog.getOpenFileName(caption=" Open File ", directory=dir, filter=filters, initialFilter=selected_filter)    
    self.show_data_excel(fname[0])
    

   #xu ly excel
  def get_cell_value_list(sheet):
    return [[cell.value for cell in row] for row in sheet] 
    
  def onCellChanged(self, row, column):
    item = self.mainHandle.table_excel.item(row, column)    
    boxcheck = item.checkState()
    if boxcheck == QtCore.Qt.CheckState.Checked:
      try:
        print("checked row: ",row)
        list = []
        for _col in range(1, self.column-1):
          item = self.mainHandle.table_excel.item(row, _col)
          list.append(item.text())
        print("row {}".format(row), str(list))
      except:
        print("no data")
    
    
  def show_data_excel(self, link):
    # link = self.form1Handle.lbl_link.toPlainText()
    self.wb = openpyxl.load_workbook(link)
    self.sheet = self.wb['Sheet1']
    # sheet_1 =self.get_cell_value_list(self.sheet[0])
    # self.sheet = self.wb.active
    
    self.mainHandle.table_excel.setRowCount(self.sheet.max_row)
    self.mainHandle.table_excel.setColumnCount(int(self.sheet.max_column)+1)
    
    self.mainHandle.table_excel.insertColumn(4)
    
    list_values = list(self.sheet.values)
    
    list_title = list(list_values[0])
    list_title.append("Status")
    list_title.append("Select")
    
    self.mainHandle.table_excel.setHorizontalHeaderLabels(list_title)
    self.row = self.mainHandle.table_excel.rowCount()
    self.column = self.mainHandle.table_excel.columnCount()
    
    
    
    row_index = 0
    for value_tuple in list_values[1:]:
      col_index = 0
      if value_tuple[0] is None:
        continue
      if "5" in str(value_tuple[1]):
        text = "update"
      else:
        text = "insert"
        
      for value in value_tuple:
          self.mainHandle.table_excel.setItem(row_index , col_index, QTableWidgetItem(str(value)))
          col_index += 1
      #status
      status = QTableWidgetItem(text)
      self.mainHandle.table_excel.setItem(row_index,col_index, status)

      #check_box
      checkbox_item = QTableWidgetItem()
      checkbox_item.setCheckState(QtCore.Qt.Unchecked)
      self.mainHandle.table_excel.setItem(row_index,col_index+1, checkbox_item)
      checkbox_item.checkState
      
      row_index += 1
        

    
  def export_data_screen_1(self):
    self.data_screen_1 = []
    for index_row in range(self.row):
      item = self.mainHandle.table_excel.item(index_row, 4)    
      if item is None: continue
      boxcheck = item.checkState()
      if boxcheck == 2 :
        list = []
        for _col in range(1, self.column-1):
          data = self.mainHandle.table_excel.item(index_row, _col)
          list.append(data.text())
        self.data_screen_1.append(list)
         
    print(self.data_screen_1)
    # print(self.row, self.column)
    

    

if __name__ == "__main__":
  app = QApplication([])
  
  ui = UI()
  
  app.exec_()