from PyQt5.QtWidgets import QTableWidgetItem, QComboBox, QMenu, QFileDialog, QWidget, QVBoxLayout, QSplitter, QPushButton, QGridLayout
from table_widget import TableWidget
from canvas_widget import CanvasWidget
from utilities import save_data, load_data
from constants import SCRIPT_DIR, FONT_PATH, DEFAULT_DIRECTORY
import pickle

class ExcelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1800, 800)
        self.layout = QVBoxLayout()
        self.sub_layout = QGridLayout()
        self.splitter = QSplitter()
        self.table = TableWidget()
        self.canvas = CanvasWidget(self.table)
        
        # 将表格和画布添加到splitter中
        self.splitter.addWidget(self.table)
        self.splitter.addWidget(self.canvas)
        self.splitter.setSizes([600, 1200])
        
        # 将splitter添加到主布局中
        self.layout.addWidget(self.splitter)
        
        self.initButtons()
        self.setLayout(self.layout)
        self.current_file_path = None
        self.default_directory = DEFAULT_DIRECTORY

        self.setWindowTitle(self.tr('Account+'))

    def initButtons(self):
        buttons = [("添加行", self.table.add_row), ("保存", self.save_data), ("另存为", self.save_data_as), ("加载", self.load_data), ("生成饼状图", self.canvas.update_pie_chart)]
        for i, (text, func) in enumerate(buttons):
            button = QPushButton(text, self)
            button.clicked.connect(func)
            self.sub_layout.addWidget(button, i // 2, i % 2)
        self.layout.addLayout(self.sub_layout)

    def save_data_as(self):  # New method for "Save As" functionality
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.default_directory, "Pickle Files (*.pkl);;All Files (*)", options=options)
        if fileName:
            if not fileName.endswith('.pkl'):
                fileName += '.pkl'
            
            data = []  # Initialize data list
            for row in range(self.table.rowCount()):  # Loop through rows in the table
                row_data = []
                for column in range(self.table.columnCount()):  # Loop through columns in each row
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
                data.append(row_data)  # Add row data to data list

            with open(fileName, 'wb') as f:
                pickle.dump(data, f)  # Save data list to file


    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        delRowAct = contextMenu.addAction("删除行")
        delRowAct.triggered.connect(self.remove_row)
        contextMenu.exec_(self.mapToGlobal(event.pos()))

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