import os
import sys
import pickle
from PyQt5.QtWidgets import (QSplitter, QMenu, QApplication, 
                             QWidget, QGridLayout, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView, QComboBox, QFileDialog)
from datetime import datetime
from collections import defaultdict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties


font = FontProperties(fname='chinese.ttf')

class ExcelApp(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1800, 800)

        self.layout = QVBoxLayout()
        self.sub_layout = QGridLayout()
        
        self.splitter = QSplitter()

        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["支出项目", "支出金额/£", "支出日期", "类型"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.splitter.addWidget(self.table) 

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.splitter.addWidget(self.canvas)
        self.splitter.setSizes([330, 500]) 

        self.layout.addWidget(self.splitter)

        self.add_row_button = QPushButton('添加行', self)
        self.add_row_button.clicked.connect(self.add_row)
        self.sub_layout.addWidget(self.add_row_button, 0, 0)

        self.save_button = QPushButton('保存', self)
        self.save_button.clicked.connect(self.save_data) 
        self.sub_layout.addWidget(self.save_button, 0, 1)

        self.save_as_button = QPushButton('另存为', self)
        self.save_as_button.clicked.connect(self.save_data_as)
        self.sub_layout.addWidget(self.save_as_button, 1, 0)

        self.load_button = QPushButton('加载', self)
        self.load_button.clicked.connect(self.load_data)
        self.sub_layout.addWidget(self.load_button, 1, 1)

        self.layout.addLayout(self.sub_layout)
        self.setLayout(self.layout)

        self.pie_chart_button = QPushButton('生成饼状图', self)
        self.pie_chart_button.clicked.connect(self.update_pie_chart)
        self.sub_layout.addWidget(self.pie_chart_button, 2, 0)

        self.current_file_path = None

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        current_date = datetime.now().strftime('%Y-%m-%d')
        date_item = QTableWidgetItem(current_date)
        self.table.setItem(row_position, 2, date_item)

        combo = QComboBox()
        combo.addItem("交通")
        combo.addItem("日用品")
        combo.addItem("学习")
        combo.addItem("日常饮食")
        combo.addItem("社交活动")
        combo.addItem("赠送")
        combo.addItem("娱乐")
        self.table.setCellWidget(row_position, 3, combo)

    def save_data_as(self):  # New method for "Save As" functionality
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", os.getcwd(), "Pickle Files (*.pkl);;All Files (*)", options=options)
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

    def update_pie_chart(self):
        self.figure.clear()
        data = defaultdict(int)
        total_expense = 0
        for row in range(self.table.rowCount()):
            category_widget = self.table.cellWidget(row, 3)
            if category_widget:
                category = category_widget.currentText()
                amount_item = self.table.item(row, 1)
                if amount_item and amount_item.text().isdigit():
                    amount = int(amount_item.text())
                    data[category] += amount
                    total_expense += amount  # Add amount to total expense

        labels = [f'{key} ({value}镑)' for key, value in data.items()]
        sizes = data.values()

        ax = self.figure.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontproperties': font, 'fontsize': 30})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display total expense at the top of the chart
        ax.text(0, 1.1, f'{total_expense}镑 <=> {total_expense * 9}元', ha='center', va='center', fontsize=50, fontproperties=font, fontweight='bold', color='red')

        self.canvas.draw()

    def remove_row(self):
        selected_indexes = self.table.selectedIndexes()
        if selected_indexes:
            rows_to_remove = set(index.row() for index in selected_indexes)
            for row in sorted(rows_to_remove, reverse=True):
                self.table.removeRow(row)

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
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Pickle Files (*.pkl);;All Files (*)", options=options)
            if fileName:
                if not fileName.endswith('.pkl'):
                    fileName += '.pkl'
                with open(fileName, 'wb') as f:
                    pickle.dump(data, f)
                self.current_file_path = fileName

    def load_data(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Pickle Files (*.pkl);;All Files (*)", options=options)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExcelApp()
    ex.show()
    sys.exit(app.exec_())
