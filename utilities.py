import pickle
from PyQt5.QtWidgets import QFileDialog, QComboBox, QTableWidgetItem

def save_data(self):
    data = []
    for row in range(self.table.rowCount()):
        row_data = []
        for column in range(self.table.columnCount()):
            if column == 3:
                combo = self.table.cellWidget(row, column)
                if combo:
                    row_data.append(combo.currentText())
                else:
                    row_data.append('')
            else:
                item = self.table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
        data.append(row_data)
    
    if self.current_file_path:
        with open(self.current_file_path, 'wb') as f:
            pickle.dump(data, f)
    else:
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", self.default_directory, "Pickle Files (*.pkl);;All Files (*)", options=options)
        if fileName:
            if not fileName.endswith('.pkl'):
                fileName += '.pkl'
            with open(fileName, 'wb') as f:
                pickle.dump(data, f)
            self.current_file_path = fileName

def load_data(self):
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", self.default_directory, "Pickle Files (*.pkl);;All Files (*)", options=options)
    if fileName:
        self.current_file_path = fileName  # 更新当前文件路径
        try:
            with open(fileName, 'rb') as f:
                data = pickle.load(f)
            
            self.table.setRowCount(len(data))
            for row, row_data in enumerate(data):
                for column, column_data in enumerate(row_data):
                    if column == 3:
                        combo = QComboBox()
                        combo.addItem("交通")
                        combo.addItem("日用品")
                        combo.addItem("学习")
                        combo.addItem("日常饮食")
                        combo.addItem("社交活动")
                        combo.addItem("赠送")
                        combo.addItem("娱乐")
                        combo.setCurrentText(column_data)
                        self.table.setCellWidget(row, column, combo)
                    else:
                        self.table.setItem(row, column, QTableWidgetItem(column_data))
        except FileNotFoundError:
            pass